\getenv owner_password MIGRATION_DB_PASSWORD
\getenv runtime_password APP_DB_PASSWORD
CREATE ROLE nour_owner LOGIN PASSWORD :'owner_password';
CREATE ROLE nour_app LOGIN PASSWORD :'runtime_password';
GRANT CONNECT ON DATABASE nour TO nour_owner, nour_app;
GRANT USAGE, CREATE ON SCHEMA public TO nour_owner;
GRANT USAGE ON SCHEMA public TO nour_app;
ALTER DEFAULT PRIVILEGES FOR ROLE nour_owner IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO nour_app;
ALTER DEFAULT PRIVILEGES FOR ROLE nour_owner IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO nour_app;
