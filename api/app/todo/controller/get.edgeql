With
    Module todo,
Select Todo {
    id,
    priority,
    title,
    status,
    description
} Filter .status != <todo::TodoStatus>"Completed" And .user.id = <uuid> global default::current_user_id ;