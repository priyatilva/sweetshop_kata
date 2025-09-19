import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import RegistrationForm from "../RegistrationForm";

// Mock fetch
global.fetch = jest.fn();

describe("RegistrationForm", () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test("renders form fields", () => {
    render(<RegistrationForm />);
    expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
  });

  test("submits form and shows success message", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    render(<RegistrationForm />);

    fireEvent.change(screen.getByPlaceholderText(/Username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Register/i }));


    await waitFor(() =>
      expect(
        screen.getByText(/Registration successful/i)
      ).toBeInTheDocument()
    );
  });
  
  test("submits form and gets success response from API", async () => {
  render(<RegistrationForm />)

  fireEvent.change(screen.getByPlaceholderText(/Username/i), {
    target: { value: "testuser" },
  })
  fireEvent.change(screen.getByPlaceholderText(/Email/i), {
    target: { value: "test@example.com" },
  })
  fireEvent.change(screen.getByPlaceholderText(/Password/i), {
    target: { value: "password123" },
  })

  fireEvent.click(screen.getByRole("button", { name: /Register/i }))

  await waitFor(() =>
    expect(screen.getByText(/User registered successfully/i)).toBeInTheDocument()
  )
})

});
