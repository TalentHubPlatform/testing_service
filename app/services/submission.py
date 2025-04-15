from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId

from repositories import (
    submission,
    problem,
    contest_repo,
    contest_result_repo
)
from .judge import JudgeService


class SubmissionService:
    def __init__(self):
        self.judge_service = JudgeService()

    def create_submission(self, user_id: int, problem_id: str, contest_id: str,
                          language: str, code: str) -> Dict[str, Any]:
        prob = problem.find_by_id(problem_id)
        if not prob:
            return {"success": False, "message": "problem not found"}

        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        submission_data = {
            "user_id": user_id,
            "problem_id": ObjectId(problem_id),
            "contest_id": ObjectId(contest_id),
            "language": language,
            "code": code,
            "submitted_at": datetime.datetime.now(datetime.UTC),
            "status": "Pending"
        }

        sub = submission.create(submission_data)

        self.judge_submission(str(sub.id))

        return {
            "success": True,
            "message": "submission created successfully",
            "submission_id": str(sub.id)
        }

    def judge_submission(self, submission_id: str) -> Dict[str, Any]:
        sub = submission.find_by_id(submission_id)
        if not sub:
            return {"success": False, "message": "submission not found"}

        submission.update(submission_id, {"status": "Judging"})

        result = self.judge_service.judge_submission(submission_id)

        if not result:
            submission.update(submission_id, {"status": "Error"})
            return {"success": False, "message": "Error while judging submission"}

        updated_submission = submission.find_with_results(submission_id)

        self._update_contest_results(str(updated_submission.contest_id), updated_submission.user_id)

        return {
            "success": True,
            "message": "submission judged successfully",
            "status": updated_submission.status
        }

    @staticmethod
    def get_submission(submission_id: str) -> Optional[Dict[str, Any]]:
        sub = submission.find_with_results(submission_id)
        if not sub:
            return None

        result = {
            "id": str(sub.id),
            "user_id": sub.user_id,
            "problem_id": str(sub.problem_id.id),
            "contest_id": str(sub.contest_id.id),
            "language": sub.language,
            "code": sub.code,
            "submitted_at": sub.submitted_at.isoformat(),
            "status": getattr(sub, "status", "Unknown"),
            "results": []
        }

        if hasattr(sub, "results"):
            for test_result in sub.results:
                result["results"].append({
                    "id": str(test_result.id),
                    "test_case_id": str(test_result.test_case_id.id),
                    "status": test_result.status,
                    "execution_time": test_result.execution_time,
                    "memory_used": test_result.memory_used,
                    "error": test_result.error
                })

        return result

    @staticmethod
    def get_user_submissions(user_id: int, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        submissions = submission.find_by_user(user_id, skip, limit)

        result = []
        for sub in submissions:
            result.append({
                "id": str(sub.id),
                "problem_id": str(sub.problem_id.id),
                "contest_id": str(sub.contest_id.id),
                "language": sub.language,
                "submitted_at": sub.submitted_at.isoformat(),
                "status": getattr(sub, "status", "Unknown")
            })

        return result

    @staticmethod
    def _update_contest_results(contest_id: str, user_id: int) -> None:
        problems = problem.find_by_contest(contest_id)
        if not problems:
            return

        total_score = 0
        solved_count = 0
        penalty = 0

        for prob in problems:
            problem_id = str(prob.id)

            user_submissions = submission.find(
                user_id=user_id,
                problem_id=ObjectId(problem_id),
                contest_id=ObjectId(contest_id)
            )

            accepted_submission = None
            for sub in user_submissions:
                if getattr(sub, "status", "") == "Accepted":
                    if not accepted_submission or sub.submitted_at < accepted_submission.submitted_at:
                        accepted_submission = sub

            if accepted_submission:
                solved_count += 1

                problem_weight = getattr(prob, "weight", 1)
                total_score += problem_weight

                # submission_time = accepted_submission.submitted_at

                attempt_penalty = user_submissions.count() - 1

                if attempt_penalty > 0:
                    penalty += attempt_penalty * 10

        contest_result_repo.update_or_create(
            contest_id,
            user_id,
            {
                "total_score": total_score,
                "solved_score": solved_count,
                "penalty": penalty
            }
        )
        