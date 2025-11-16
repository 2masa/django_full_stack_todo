With
    Module todo,
Update Todo Filter .id = <uuid>$id
Set {
    description := <optional str>$description ?? .description,
    title := <optional str>$title ?? .title,
    priority := <optional todo::TodoPriorityStatus>$priority ?? .priority,
    status := <optional todo::TodoStatus>$status ?? .status,
};