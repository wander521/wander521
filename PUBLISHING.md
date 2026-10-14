# GitHub profile publishing

This repository supplies the profile README for `https://github.com/wander521`.

- `README.md`: default English profile.
- `README-zh.md`: equivalent Chinese version, linked from the default profile.
- `README-en.md`: English compatibility entry.
- `assets/hero-closeup.gif`: close-up robot loop derived from the owner's reference recording.
- `assets/hero-closeup.png`: reduced-motion fallback.
- `assets/CREDITS.md`: model and font attribution, with included license files.

The profile repository must be **public** and named **wander521/wander521**. Its root README.md is displayed on the account page. Publishing these files does not rebuild or modify the separate personal website.

Update through ordinary Git commits and a fast-forward push. Preserve any existing remote history; inspect and fetch the current remote branch before the first push. Never force-push to replace an existing repository.

Local visual QA uses a Markdown approximation. Final GitHub rendering, language links and image URLs must be verified after publishing.

The public contribution snake is maintained by `.github/workflows/activity.yml` on a daily schedule and when its source changes. It only commits the activity SVGs and public calendar snapshot; it uses the repository's built-in GitHub token and needs no personal access token.
