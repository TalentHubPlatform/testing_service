from typing import Dict, List, Optional, Any

from repositories import (
    contest_repo,
    contest_language_repo,
    contest_result_repo
)


class ContestService:
    @staticmethod
    def create_contest(name: str, description: str = None,
                       event_id: int = None, date_id: int = None,
                       track_id: int = None) -> Dict[str, Any]:
        existing = contest_repo.find_by_name(name)
        if existing:
            return {"success": False, "message": "Contest with this name already exists"}

        contest_data = {
            "name": name,
            "description": description,
            "event_id": event_id,
            "date_id": date_id,
            "track_id": track_id,
            "is_active": True
        }

        contest = contest_repo.create(contest_data)

        return {
            "success": True,
            "message": "Contest created successfully",
            "contest_id": str(contest.id)
        }

    @staticmethod
    def update_contest(contest_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        if "name" in data and data["name"] != contest.name:
            existing = contest_repo.find_by_name(data["name"])
            if existing and str(existing.id) != contest_id:
                return {"success": False, "message": "Contest with this name already exists"}

        updated_contest = contest_repo.update(contest_id, data)

        if not updated_contest:
            return {"success": False, "message": "Error updating contest"}

        return {
            "success": True,
            "message": "Contest updated successfully",
            "contest_id": contest_id
        }

    @staticmethod
    def delete_contest(contest_id: str) -> Dict[str, Any]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        result = contest_repo.delete(contest_id)

        if not result:
            return {"success": False, "message": "Error deleting contest"}

        return {
            "success": True,
            "message": "Contest deleted successfully"
        }

    @staticmethod
    def get_contest(contest_id: str) -> Optional[Dict[str, Any]]:
        contest = contest_repo.find_with_problems(contest_id)
        if not contest:
            return None

        languages = contest_language_repo.find_languages_for_contest(contest_id)

        result = {
            "id": str(contest.id),
            "name": contest.name,
            "description": contest.description,
            "event_id": contest.event_id,
            "date_id": contest.date_id,
            "track_id": contest.track_id,
            "is_active": contest.is_active,
            "problems": [],
            "languages": []
        }

        if hasattr(contest, "problems"):
            for problem in contest.problems:
                result["problems"].append({
                    "id": str(problem.id),
                    "title": problem.title,
                    "description": problem.description,
                    "time_limit": problem.time_limit,
                    "memory_limit": problem.memory_limit
                })

        for language in languages:
            result["languages"].append({
                "id": str(language.id),
                "name": language.name,
                "version": language.version
            })

        return result

    @staticmethod
    def get_contests(skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        contests = contest_repo.find_all(skip, limit)

        result = []
        for contest in contests:
            result.append({
                "id": str(contest.id),
                "name": contest.name,
                "description": contest.description,
                "event_id": contest.event_id,
                "date_id": contest.date_id,
                "track_id": contest.track_id,
                "is_active": contest.is_active
            })

        return result

    @staticmethod
    def add_language_to_contest(contest_id: str, language_id: str) -> Dict[str, Any]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        try:
            contest_language_repo.add_language_to_contest(contest_id, language_id)
            return {
                "success": True,
                "message": "Language added to contest successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding language to contest: {str(e)}"}

    @staticmethod
    def remove_language_from_contest(contest_id: str, language_id: str) -> Dict[str, Any]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        result = contest_language_repo.remove_language_from_contest(contest_id, language_id)

        if result:
            return {
                "success": True,
                "message": "Language removed from contest successfully"
            }
        else:
            return {"success": False, "message": "Error removing language from contest"}

    @staticmethod
    def get_contest_results(contest_id: str) -> List[Dict[str, Any]]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return []

        results = contest_result_repo.find_by_contest(contest_id)

        result = []
        for r in results:
            result.append({
                "user_id": r.user_id,
                "total_score": r.total_score,
                "solved_score": r.solved_score,
                "penalty": r.penalty
            })

        result.sort(key=lambda x: (-x["total_score"], x["penalty"]))

        for i, r in enumerate(result):
            r["rank"] = i + 1

        return result

    @staticmethod
    def find_contests_by_track(track_id: int) -> List[Dict[str, Any]]:
        contests = contest_repo.find(track_id=track_id)

        result = []
        for contest in contests:
            result.append({
                "id": str(contest.id),
                "name": contest.name,
                "description": contest.description,
                "event_id": contest.event_id,
                "date_id": contest.date_id,
                "track_id": contest.track_id,
                "is_active": contest.is_active
            })

        return result

    @staticmethod
    def finish_contests_by_track(track_id: int) -> Dict[str, Any]:
        contests = contest_repo.find(track_id=track_id, is_active=True)

        finished_count = 0
        for contest in contests:
            contest_repo.update(str(contest.id), {"is_active": False})
            finished_count += 1

        return {
            "success": True,
            "message": f"Successfully finished {finished_count} contests for track {track_id}",
            "finished_count": finished_count
        }
