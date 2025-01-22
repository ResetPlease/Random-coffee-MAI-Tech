package models

type UserType string

var (
	Student  UserType = "student"  // просто студент
	Admin    UserType = "admin"    // администратор
	Academic UserType = "academic" // преподаватель (на будущее)
)

type User struct {
	ID       uint64
	Type     UserType
	Name     string
	LastName string
	Group    string
	Email    string
}
