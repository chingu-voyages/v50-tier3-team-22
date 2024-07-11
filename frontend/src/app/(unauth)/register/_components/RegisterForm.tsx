"use client";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkboxMk1";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { fastApi } from "@/lib/axios";
import { registerSchema, UserRegisterType } from "@/lib/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { CheckIcon } from "@radix-ui/react-icons";
import { useMutation } from "@tanstack/react-query";
import axios, { AxiosError } from "axios";
import { redirect } from "next/navigation";
import React, { useEffect } from "react";
import { useForm } from "react-hook-form";

export default function RegisterForm() {
  const form = useForm<UserRegisterType>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      terms: false,
    },
  });

  const mutattion = useMutation({
    mutationFn: (data: UserRegisterType) => {
      return axios.post("/auth/register", data);
    },
  });

  async function onSubmit(data: UserRegisterType) {
    try {
      const response = await mutattion.mutateAsync(data);
      if (response?.status === 201) {
        redirect(`/login?email=${response?.data.email}`);
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        form.setError("root", { message: error.message });
      } else {
        form.setError("root", { message: "Something went wrong" });
      }
    } finally {
      console.log("finally");
    }
  }

  return (
    <div>
      {form.formState.errors.root && (
        <p className="text-red-500">{form.formState.errors.root.message}</p>
      )}
      <Form {...form}>
        <form
          className="flex flex-col gap-5"
          onSubmit={form.handleSubmit(onSubmit)}
        >
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem className="space-y-0">
                <FormLabel className="text-sm">Name</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Enter your name"
                    {...field}
                    className="text-[10px] leading-4 px-2 h-8"
                  />
                </FormControl>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem className="space-y-0">
                <FormLabel className="text-sm">Email address</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Enter your email"
                    {...field}
                    className="text-[10px] leading-4 px-2 h-8"
                  />
                </FormControl>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem className="space-y-0">
                <FormLabel className="text-sm">Password</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Enter your password"
                    type="password"
                    {...field}
                    className="text-[10px] leading-4 px-2 h-8"
                  />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="terms"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    className="rounded-[2px] h-3 w-3"
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  >
                    <CheckIcon className="h-3 w-3" />
                  </Checkbox>
                </FormControl>
                <FormLabel className="text-[10px]">
                  I agree with the terms and conditions
                </FormLabel>
                <FormLabel></FormLabel>
              </FormItem>
            )}
          />
          <Button type="submit" className="hover:text-primary">
            Signup
          </Button>
        </form>
      </Form>
    </div>
  );
}
