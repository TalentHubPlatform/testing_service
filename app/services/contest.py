from typing import Dict, List, Optional, Any

from repositories import (
    contest,
    contest_language,
    contest_result
)


class ContestService:
    @staticmethod
    def create_contest(name: str, description: str = None,
                       event_id: int = None, date_id: int = None) -> Dict[str, Any]:
        existing = contest.find_by_name(name)

        if existing:
            return {"success": False, "message": "contest with this name already exists"}

        contest_data = {
            "name": name,
            "description": description,
            "event_id": event_id,
            "date_id": date_id
        }

        cont = contest.create(contest_data)

        return {
            "success": True,
            "message": "contest created successfully",
            "contest_id": str(cont.id)
        }

    @staticmethod
    def update_contest(contest_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        cont = contest.find_by_id(contest_id)

        if not cont:
            return {"success": False, "message": "contest not found"}

        if "name" in data and data["name"] != cont.name:
            existing = contest.find_by_name(data["name"])

            if existing and str(existing.id) != contest_id:
                return {"success": False, "message": "contest with this name already exists"}

        updated_contest = contest.update(contest_id, data)

        if not updated_contest:
            return {"success": False, "message": "Error updating contest"}

        return {
            "success": True,
            "message": "contest updated successfully",
            "contest_id": contest_id
        }

    @staticmethod
    def delete_contest(contest_id: str) -> Dict[str, Any]:
        cont = contest.find_by_id(contest_id)
        if not cont:
            return {"success": False, "message": "contest not found"}

        result = contest.delete(contest_id)

        if not result:
            return {"success": False, "message": "Error deleting contest"}

        return {
            "success": True,
            "message": "contest deleted successfully"
        }

    @staticmethod
    def get_contest(contest_id: str) -> Optional[Dict[str, Any]]:
        cont = contest.find_with_problems(contest_id)
        if not cont:
            return None

        languages = contest_language.find_languages_for_contest(contest_id)

        result = {
            "id": str(cont.id),
            "name": cont.name,
            "description": cont.description,
            "event_id": cont.event_id,
            "date_id": cont.date_id,
            "problems": [],
            "languages": []
        }

        if hasattr(cont, "problems"):
            for prob in cont.problems:
                result["problems"].append({
                    "id": str(prob.id),
                    "title": prob.title,
                    "description": prob.description,
                    "time_limit": prob.time_limit,
                    "memory_limit": prob.memory_limit
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
        contests = contest.find_all(skip, limit)

        result = []

        for cont in contests:
            result.append({
                "id": str(cont.id),
                "name": cont.name,
                "description": cont.description,
                "event_id": cont.event_id,
                "date_id": cont.date_id
            })

        return result

    @staticmethod
    def add_language_to_contest(contest_id: str, language_id: str) -> Dict[str, Any]:
        cont = contest.find_by_id(contest_id)
        if not cont:
            return {"success": False, "message": "contest not found"}

        try:
            contest_language.add_language_to_contest(contest_id, language_id)
            return {
                "success": True,
                "message": "Language added to contest successfully"
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding language to contest: {str(e)}"}

    @staticmethod
    def remove_language_from_contest(contest_id: str, language_id: str) -> Dict[str, Any]:
        cont = contest.find_by_id(contest_id)
        if not cont:
            return {"success": False, "message": "contest not found"}

        result = contest_language.remove_language_from_contest(contest_id, language_id)

        if result:
            return {
                "success": True,
                "message": "Language removed from contest successfully"
            }
        else:
            return {"success": False, "message": "Error removing language from contest"}

    @staticmethod
    def get_contest_results(contest_id: str) -> List[Dict[str, Any]]:
        cont = contest.find_by_id(contest_id)

        if not cont:
            return []

        results = contest_result.find_by_contest(contest_id)

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
