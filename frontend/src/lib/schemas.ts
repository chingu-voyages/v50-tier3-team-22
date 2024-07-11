import { z } from "zod";

export const registerSchema = z.object({
  name: z.string().min(1, { message: "Name is required" }),
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email" }),
  password: z
    .string()
    .min(1, { message: "Password is required" })
    .min(6, { message: "Password must be at least 6 characters" }),
  terms: z
    .boolean()
    .default(false)
    .refine((val) => val, {
      message: "You must agree to the terms and conditions",
    }),
});

export type UserRegisterType = z.infer<typeof registerSchema>;
