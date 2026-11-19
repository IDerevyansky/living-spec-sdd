# Prompt: review a pull request

The argument is a pull request number. You review; you never commit or push.

1. Get the pull request and its diff (`gh pr view <n>` and `gh pr diff <n>`,
   or the GitHub API).
2. Find its task in the change folder and the criteria it covers in the living
   specs.
3. Go through `docs/workflow/review-checklist.md` for its kind.
4. Report in the owner's language:
   - verdict: ready to merge / changes needed / stop (rule broken);
   - findings with file and line, most important first;
   - questions for the owner.
5. Post the report as a pull request comment only if the owner asks.
