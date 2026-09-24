from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from datasets.models import Dataset
from signals.models import Signal
from scenarios.models import Scenario
from decisions.models import Decision
from recommendations.models import Recommendation


class DashboardSummaryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_projects_count = Project.objects.count()
        datasets_count = Dataset.objects.count()
        active_signals_count = Signal.objects.filter(status='active').count()
        high_risk_signals_count = Signal.objects.filter(severity__in=['high', 'critical']).count()
        scenarios_count = Scenario.objects.count()
        decisions_count = Decision.objects.count()

        top_recommendation = Recommendation.objects.order_by('-score', '-expected_impact').first()
        top_rec_data = None
        if top_recommendation:
            top_rec_data = {
                "id": top_recommendation.id,
                "title": top_recommendation.title,
                "expected_impact": top_recommendation.expected_impact,
                "risk_level": top_recommendation.risk_level,
                "score": top_recommendation.score,
                "scenario_name": top_recommendation.scenario.name,
            }

        return Response({
            "overview": {
                "active_projects": active_projects_count,
                "datasets": datasets_count,
                "active_signals": active_signals_count,
                "high_risk_signals": high_risk_signals_count,
                "scenarios_tested": scenarios_count,
                "decisions_made": decisions_count,
            },
            "top_recommended_action": top_rec_data
        })