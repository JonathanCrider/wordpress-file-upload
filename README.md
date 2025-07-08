# WordPress File Upload

Automatically upload files to WordPress and move them to new folder when successful.

## Dependencies

- [node](https://nodejs.org/en)
- [dotenv](https://www.npmjs.com/package/dotenv)
- [playwright](https://www.npmjs.com/package/playwright)
  - don't forget to `npx playwright install-deps`
- a `.env` with the following variables

```bashh 
WORDPRESS_USERNAME=
WORDPRESS_PASSWORD=
WORDPRESS_SITE=
ROOT_DIRECTORY=
DIRECTORY=
DESTINATION=
```
