# Holidays｜节假日 — Apple Calendar subscription

This project creates a public, read-only `.ics` feed with common international holidays (2026–2035) and Chinese official holiday/rest-day and make-up workday adjustments **only for years where verified data is available**.

## Publish (GitHub Pages)

1. Sign in to GitHub and create a **public** repository named `holidays` (or another name).
2. Upload **all** project files, including `.github/workflows/update.yml`, to the `main` branch. If GitHub's web uploader does not preserve hidden folders, use the GitHub web editor to create `.github/workflows/update.yml` manually.
3. Go to **Settings → Pages → Build and deployment**, select **Deploy from a branch**, choose `main` and `/ (root)`, and save.
4. Once Pages finishes publishing, subscribe in Apple Calendar to `https://YOUR_USERNAME.github.io/holidays/holidays.ics` (replace username and repository name as needed).
5. In **Actions**, enable workflows if GitHub asks. The workflow checks daily for updated Chinese holiday schedules. Run **Update holiday subscription → Run workflow** once to populate Chinese official data immediately.

## Notes

- China holiday data comes from the community-maintained [NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn) annual JSON records based on official announcements. **This is not an official government API.** Verify against State Council announcements for critical scheduling.
- Future years are not guessed: until announced, Chinese official rest/make-up workday entries for that year will be absent.
- International dates include Easter (computus), US Thanksgiving, Mother's Day (second Sunday of May), Father's Day (third Sunday of June), and fixed-date holidays.
- Calendar subscription refresh intervals are controlled by the calendar client; changes are not necessarily instant.
- If your repository is named something other than `holidays`, adjust the URL accordingly.
Additional calendar: school(3).ics — School Timetable.
