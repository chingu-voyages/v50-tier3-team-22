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

export const AddRecipeSchema = z.object({
  name: z
    .string({ required_error: "Title is required" })
    .min(5, { message: "Title must be at least 5 characters" }),
  cuisine: z
    .string({ required_error: "Cuisine is required" })
    .min(5, { message: "Cuisine must be at least 5 characters" }),
  time: z.number({ required_error: "Time is required" }),
  level: z.number({ required_error: "Level is required" }),
  category: z.number({ required_error: "Category is required" }),
  description: z
    .string({ required_error: "Description is required" })
    .min(1, { message: "Description is required" }),
  image: z
    .string({ required_error: "Image is required" })
    .url({ message: "Image is required" }),
  // ingredients: z
  //   .array(
  //     z.object({
  //       name: z.string().min(1, { message: "Name is required" }),
  //       type: z.string().min(1, { message: "Type is required" }),
  //       unit: z.string().min(1, { message: "Unit is required" }),
  //       amount: z.number().min(1, { message: "Amount is required" }),
  //     })
  //   )
  //   .min(1, { message: "At least 1 ingredient is required" }),
});

export type UserRegisterType = z.infer<typeof registerSchema>;
export type AddRecipeType = z.infer<typeof AddRecipeSchema>;
