CREATE MIGRATION m1ji7cddvh2y2jfgubgp2djsimupk5jq37gyckc2o6hq5drphgrs3a
    ONTO initial
{
  CREATE MODULE todo IF NOT EXISTS;
  CREATE MODULE user IF NOT EXISTS;
  CREATE SCALAR TYPE todo::TodoPriorityStatus EXTENDING enum<Highest, High, Medium, Low>;
  CREATE SCALAR TYPE todo::TodoStatus EXTENDING enum<Open, Completed, Pending, InProgress, Cancelled>;
  CREATE FUTURE nonrecursive_access_policies;
  CREATE GLOBAL default::current_user_id -> std::uuid;
  CREATE TYPE default::AuditLog {
      CREATE REQUIRED LINK entity: std::Object {
          ON TARGET DELETE DELETE SOURCE;
          SET readonly := true;
      };
      CREATE REQUIRED PROPERTY action: std::str {
          SET readonly := true;
      };
      CREATE REQUIRED PROPERTY timestamp: std::datetime {
          SET default := (std::datetime_current());
          SET readonly := true;
      };
  };
  CREATE ABSTRACT TYPE user::UserType {
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE REQUIRED PROPERTY clean_email: std::str {
          SET default := (std::str_trim(std::str_lower(.email)));
      };
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON (.email) {
          SET errmessage := 'User email already exists.';
          CREATE ANNOTATION std::title := 'User email details';
      };
  };
  ALTER TYPE default::AuditLog {
      CREATE REQUIRED LINK user: user::UserType {
          SET default := (SELECT
              user::UserType
          FILTER
              (.id = GLOBAL default::current_user_id)
          );
          ON TARGET DELETE DELETE SOURCE;
          SET readonly := true;
      };
  };
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::AuditLog
              {
                  entity := __new__,
                  action := 'insert'
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH DO (INSERT
              default::AuditLog
              {
                  entity := __new__,
                  action := 'update'
              });
  };
  CREATE TYPE todo::Todo EXTENDING default::Auditable {
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY priority: todo::TodoPriorityStatus;
      CREATE REQUIRED PROPERTY status: todo::TodoStatus;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE TYPE user::Credential EXTENDING default::Auditable {
      CREATE LINK user: user::UserType {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY last_changed: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY password: std::bytes;
  };
  CREATE TYPE user::User EXTENDING user::UserType, default::Auditable {
      CREATE REQUIRED PROPERTY phone_number: std::str;
  };
  ALTER TYPE todo::Todo {
      CREATE REQUIRED LINK user: user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  CREATE TYPE user::RootUser EXTENDING user::UserType {
      ALTER PROPERTY email {
          SET default := 'rootadmin@todo.com';
          SET OWNED;
          SET REQUIRED;
          SET TYPE std::str;
      };
      ALTER PROPERTY name {
          SET default := "Todo's Root User";
          SET OWNED;
          SET REQUIRED;
          SET TYPE std::str;
      };
  };
};
