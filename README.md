# WordPress File Upload

Automatically upload files to WordPress and move them to new folder when successful.

## Dependencies

- [node](https://nodejs.org/en)
- [dotenv](https://www.npmjs.com/package/dotenv)
- [playwright](https://www.npmjs.com/package/playwright)
  - don't forget to `npx playwright install-deps`
- a `.env` with the following variables

```bash
WORDPRESS_USERNAME=
WORDPRESS_PASSWORD=
WORDPRESS_SITE=<yoursite.com>
ROOT_DIRECTORY=<path/to/directory/>
DIRECTORY=<to/main/directory>
DESTINATION=<to/final/destination>
```

**NOTES:**

- My path includes the current year, modify the code to fit your file structure.
- Also note the location of `/` characters in the url strings to construct a correct path.
- This script moves the file to a different directory after upload, that way we don't upload duplicate files.
