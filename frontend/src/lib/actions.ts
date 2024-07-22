"use server";

export type State = {
  status: "success" | "error";
  message: string;
} | null;

export async function registerAction(
  prevState: State,
  data: FormData
): Promise<State> {
  await new Promise((resolve) => setTimeout(resolve, 2000));

  console.log("registerAction");

  return {
    status: "success",
    message: `Successfully registered!`,
  };
}
