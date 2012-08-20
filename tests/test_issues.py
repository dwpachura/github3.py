import base
import github3
from expecter import expect
from datetime import datetime
from github3.users import User
from github3.issues import Issue, IssueComment, IssueEvent, Label, Milestone


class TestIssues(base.BaseTest):
    def test_issue(self):
        issue = self.g.issue(self.sigm, self.todo, '2')
        with expect.raises(github3.GitHubError):
            issue.close()
            issue.add_labels('foo', 'bar')
            issue.edit('Foo', 'Bar', self.sigm, 'closed')
            issue.remove_label('Bug')
            issue.remove_all_labels()
            issue.repoen()

        expect(issue).isinstance(Issue)

        if issue.assignee:
            expect(issue.assignee).isinstance(User)

        expect(issue.body).isinstance((str, bytes))
        expect(issue.created_at).isinstance(datetime)
        expect(issue.closed_at).isinstance(datetime)
        expect(issue.comment(2965299)).isinstance(IssueComment)
        expect(issue.html_url).isinstance((str, bytes))
        expect(issue.id) > 0
        expect(issue.is_closed()).isinstance(bool)

        for label in issue.labels:
            expect(label).isinstance(Label)

        for ev in issue.list_events():
            expect(ev).isinstance(IssueEvent)

        if issue.milestone:
            expect(issue.milestone).isinstance(Milestone)

        for com in issue.list_comments():
            expect(com).isinstance(IssueComment)

        expect(issue.number) > 0
        expect(issue.pull_request).isinstance(dict)
        expect(issue.repository).isinstance(tuple)
        expect(issue.state).isinstance(tuple)

        if issue.state not in ('open', 'closed'):
            self.fail('State not valid')

        if issue.title:
            expect(issue.title).isinstance((str, bytes))

        expect(issue.updated_at).isinstance(datetime)
        expect(issue.user).isinstance(User)
