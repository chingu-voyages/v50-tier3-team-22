"use client";
import UploadImage from "@/components/Layout/newRecipe/UploadImage";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { fastApi } from "@/lib/axios";
import { AddRecipeSchema, AddRecipeType } from "@/lib/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import React from "react";
import { useForm } from "react-hook-form";

export default function AddRecipeForm({ categories, levels }: any) {
  const router = useRouter();

  const form = useForm<AddRecipeType>({
    resolver: zodResolver(AddRecipeSchema),
  });

  async function onSubmit(data: AddRecipeType) {
    console.log({ data });
    try {
      const response = await fastApi.post("/recipe", data);
      if (response?.status === 201) {
        router.push(`/recipes`);
      } else {
        form.setError("root", { message: "Something went wrong" });
        console.log("error");
      }
    } catch (error) {
      form.setError("root", { message: "Something went wrong" });
      console.log(error);
    }
  }
  return (
    <Form {...form}>
      <form
        className="flex flex-col gap-16 px-20 py-16 w-full"
        onSubmit={form.handleSubmit(onSubmit)}
      >
        <div className="flex justify-between px-7">
          <h2 className="text-3xl font-medium">Add Recipe</h2>
          <Button className="text-base px-10 py-2">Save Recipe</Button>
        </div>
        <div className="flex flex-col w-full bg-white rounded p-7 gap-16">
          <div className="flex w-full gap-9">
            <div className="w-fit ">
              <div className="w-80 h-52 bg-gray-100 rounded">
                <FormField
                  control={form.control}
                  name="image"
                  render={({ field }) => (
                    <FormItem className="w-full h-full">
                      <UploadImage
                        register={form.register}
                        setValue={form.setValue}
                      />
                    </FormItem>
                  )}
                />
                {form.formState.errors.image && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.image.message}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-6 w-full">
              <div className="col-span-2 w-full rounded-sm">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Title</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Enter your recipe title"
                          {...field}
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                {form.formState.errors.name && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.name.message}
                  </p>
                )}
              </div>
              <div className="w-full rounded-sm ">
                {" "}
                <FormField
                  control={form.control}
                  name="category"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Category</FormLabel>
                      <Select onValueChange={field.onChange}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select a Category" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {Object.entries(categories).map(([key, name]) => (
                            <SelectItem key={key} value={name as string}>
                              {name as string}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </FormItem>
                  )}
                />
                {form.formState.errors.category && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.category.message}
                  </p>
                )}
              </div>
              <div className="w-full rounded-sm ">
                <FormField
                  control={form.control}
                  name="cuisine"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Cusine</FormLabel>
                      <FormControl>
                        <Input placeholder="Select a Cuisine" {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
                {form.formState.errors.cuisine && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.cuisine.message}
                  </p>
                )}
              </div>
              <div className="w-full rounded-sm ">
                <FormField
                  control={form.control}
                  name="level"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Level</FormLabel>
                      <Select onValueChange={field.onChange}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select the dificulty level" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {Object.entries(levels).map(([key, name]) => (
                            <SelectItem key={key} value={name as string}>
                              {name as string}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </FormItem>
                  )}
                />
                {form.formState.errors.level && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.level.message}
                  </p>
                )}
              </div>
              <div className="w-full rounded-sm ">
                <FormField
                  control={form.control}
                  name="time"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Time</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Duration in minutes"
                          {...field}
                          type="number"
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                {form.formState.errors.time && (
                  <p className="text-red-500 text-xs">
                    {form.formState.errors.time.message}
                  </p>
                )}
              </div>
            </div>
          </div>
          <div className="w-full rounded-sm ">
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter your recipe description"
                      {...field}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>
        </div>
      </form>
    </Form>
  );
}
