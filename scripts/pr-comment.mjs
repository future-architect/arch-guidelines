/**
 * Used in `/.github/workflows/test-build-resources-with-pandoc.yml`
 * @param {object} params
 * @param {import('@actions/github/lib/utils').GitHub} params.github
 * @param {import('@actions/github/lib/context').Context} params.context
 * @param {string} params.url
 */
export async function postCustomForArchiveResources({ github, context, url }) {
  const sha =
    context.eventName === "pull_request"
      ? context.payload.pull_request.head.sha
      : context.payload.after;
  const commitUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/commit/${sha}`;

  const pullRequestNumber = await getPullRequestNumber();

  const botCommentIdentifier =
    "<!-- posted by scripts/pr-comment.mjs#postCustomForArchiveResources -->";

  const body = `${botCommentIdentifier}
  
  ## Pandocで生成したリソースの確認
  
  <${url}>
  
  ---
  
  [View Commit](${commitUrl})`;

  if (pullRequestNumber) {
    await createOrUpdateComment(pullRequestNumber);
  } else {
    console.log(
      "No open pull request found for this push. Logging publish information to console:",
    );
    console.log(`\n${"=".repeat(50)}`);
    console.log(body);
    console.log(`\n${"=".repeat(50)}`);
  }

  async function getPullRequestNumber() {
    if (context.eventName === "pull_request") {
      if (context.issue.number) {
        return context.issue.number;
      }
    } else if (context.eventName === "push") {
      const pullRequests = await github.rest.pulls.list({
        owner: context.repo.owner,
        repo: context.repo.repo,
        state: "open",
        head: `${context.repo.owner}:${context.ref.replace("refs/heads/", "")}`,
      });

      if (pullRequests.data.length > 0) {
        return pullRequests.data[0].number;
      }
    }

    return null;
  }

  async function findBotComment(issueNumber) {
    const comments = await github.rest.issues.listComments({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: issueNumber,
    });

    return comments.data.find((comment) =>
      comment.body.includes(botCommentIdentifier),
    );
  }

  async function createOrUpdateComment(issueNumber) {
    const existingComment = await findBotComment(issueNumber);

    if (existingComment) {
      await github.rest.issues.updateComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        comment_id: existingComment.id,
        body,
      });
    } else {
      await github.rest.issues.createComment({
        issue_number: issueNumber,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body,
      });
    }
  }
}
