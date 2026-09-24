"""API Views for Authentication, Email Code Verification, and Password Reset."""
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, VerificationCode
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    VerifyEmailCodeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


def send_otp_email(to_email, username, code, subject, action_name):
    """Utility to dispatch a clean 6-digit code email."""
    message = (
        f"Hello {username},\n\n"
        f"Your 6-digit verification code for {action_name} is:\n\n"
        f"    {code}\n\n"
        f"This code will expire in 15 minutes.\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"— RIPPLE Decision-Support Platform"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False
    )


class RegisterAPIView(APIView):
    """Registers user and emails a 6-digit verification code."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and send 6-digit verification code
        code_obj = VerificationCode.create_code(user, 'email_verification')
        send_otp_email(
            to_email=user.email,
            username=user.username,
            code=code_obj.code,
            subject="Verify your RIPPLE Account",
            action_name="Email Verification"
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "User registered. A 6-digit verification code has been sent to your email.",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_201_CREATED
        )


class VerifyEmailAPIView(APIView):
    """Verifies user's email using a 6-digit code."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"error": "No account associated with this email."}, status=status.HTTP_404_NOT_FOUND)

        code_entry = VerificationCode.objects.filter(
            user=user,
            code=code,
            purpose='email_verification',
            is_used=False
        ).first()

        if not code_entry or not code_entry.is_valid():
            return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)

        code_entry.is_used = True
        code_entry.save()

        user.is_email_verified = True
        user.save()

        return Response({"message": "Email successfully verified!"}, status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(APIView):
    """Sends a 6-digit password reset code to user's email."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = CustomUser.objects.filter(email__iexact=email).first()
        if user:
            code_obj = VerificationCode.create_code(user, 'password_reset')
            send_otp_email(
                to_email=user.email,
                username=user.username,
                code=code_obj.code,
                subject="RIPPLE Password Reset Code",
                action_name="Password Reset"
            )

        return Response(
            {"message": "If an account exists with this email, a 6-digit reset code has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmAPIView(APIView):
    """Resets password using the 6-digit code."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

        code_entry = VerificationCode.objects.filter(
            user=user,
            code=code,
            purpose='password_reset',
            is_used=False
        ).first()

        if not code_entry or not code_entry.is_valid():
            return Response({"error": "Invalid or expired reset code."}, status=status.HTTP_400_BAD_REQUEST)

        code_entry.is_used = True
        code_entry.save()

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully. You can now log in."}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful.",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required to logout."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK
        )


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user