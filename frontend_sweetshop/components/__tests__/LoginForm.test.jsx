import { render, screen, fireEvent } from "@testing-library/react"
import LoginForm from "../LoginForm"

describe("LoginForm", () => {
  test("renders login form fields", () => {
    render(<LoginForm />)

    expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument()
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument()
  })

  test("shows success message after submit", () => {
    render(<LoginForm />)

    fireEvent.change(screen.getByPlaceholderText(/Username/i), {
      target: { value: "testuser" },
    })
    fireEvent.change(screen.getByPlaceholderText(/Password/i), {
      target: { value: "password123" },
    })

    fireEvent.click(screen.getByRole("button", { name: /login/i }))

    expect(screen.getByText(/Login successful/i)).toBeInTheDocument()
  })
})
