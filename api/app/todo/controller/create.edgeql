With
    Module todo,
Insert Todo {
    description := <std::str>$description,
    title := <std::str>$title,
    priority := <todo::TodoPriorityStatus>$priority,
    status := <todo::TodoStatus>$status,
    user := (Select user::User Filter  .id = <uuid>global default::current_user_id )
};