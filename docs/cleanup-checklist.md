# Cleanup Checklist: thryve-lp-sourcing Test Credentials

Work through this list top to bottom if you stop using this project or want to remove the test credentials.

## Slack

- [ ] Delete the Slack app at https://api.slack.com/apps (Basic Information, then Delete App). This revokes the bot token.
- [ ] Remove the `SLACK_BOT_TOKEN` line from `~/.zshrc`.
- [ ] Delete the test channel, if you created one only for this project.

## Google

- [ ] Delete the OAuth client in Google Cloud Console (APIs & Services, then Credentials).
- [ ] Remove the app's access at https://myaccount.google.com/permissions.
- [ ] Delete `google_cred.json` from `~/Projects/thryve-lp-sourcing`.
- [ ] Delete any Gmail or Drive token file the agent created in the project folder.
- [ ] Shut down the Google Cloud project (project settings, then Shut down) if you will not use it again.

## Local files

- [ ] Confirm no copies of `google_cred.json` remain on your Desktop or in Downloads.
- [ ] Confirm `.gitignore` still lists the credential and token files. Keep it if you keep the repo.

## Verify

- [ ] Open a new Terminal window and run `[ -n "$SLACK_BOT_TOKEN" ] && echo "set" || echo "missing"`. It should say `missing`.
- [ ] Run `git status` in the project folder. No credential files should appear.

## Notes

- If you keep the repo but stop the experiment, you only need the Slack and Google items. The `.gitignore` and repo can stay.
- Consider adding a line to LEARNING.md noting the date the test credentials were deleted.
