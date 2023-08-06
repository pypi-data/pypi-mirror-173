import gitlab
from decouple import config
from gitlab.v4.objects import ProjectIssue, Project

from ticket_cross_check.gitlab_models import GitlabIssue


class GitlabConnector:
    def __init__(self, personal_api_token: str, project_id: str):
        """
        Create Gitlab instance with token and project
        :param personal_api_token:
        :param project_id:
        """
        assert personal_api_token
        assert project_id
        self.project_id = project_id
        self.__gitlab = gitlab.Gitlab(private_token=personal_api_token)

    @staticmethod
    def factory() -> "GitlabConnector":
        personal_api_token = config('PRIVATE_TOKEN')
        project_id = config('PROJECT_ID', default=False)
        if not project_id:
            # if project is not defined, assume current project
            project_id = config('CI_PROJECT_ID')
        return GitlabConnector(personal_api_token, project_id)

    @property
    def project(self):
        return self.__gitlab.projects.get(self.project_id)

    def get_issues(self, state: str = None, labels: list[str] = None, order_by="created_at", sort="desc"):
        """
        Get filtered list of issues
        implements #31
        :param state: "opened", "closed", None
        :param labels: list or None = all
        :param order_by:
        :param sort:
        :return:
        """
        args = {'order_by': order_by, 'sort': sort, 'iterator': True}
        if state:
            args['state'] = state
        if labels:
            args['labels'] = labels
        issues_iter = self.project.issues.list(**args)
        return self._convert_issues(issues_iter)

    @staticmethod
    def _convert_issues(issue_json: list[ProjectIssue]) -> set[GitlabIssue]:
        result = set()
        for raw_req in issue_json:
            result.add(GitlabIssue.from_project_issue(raw_req))
        return result

    @staticmethod
    def _convert_issues_from_dict(issue_json: list[dict]) -> set[GitlabIssue]:
        result = set()
        for raw_req in issue_json:
            result.add(GitlabIssue(**raw_req))
        return result

    def get_project(self) -> Project:
        """Get GitlabProject info from API"""
        rpi = self.__gitlab.projects.get(self.project_id)
        return rpi
