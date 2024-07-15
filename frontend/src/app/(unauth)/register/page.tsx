import React from "react";
import RegisterForm from "./_components/RegisterForm";
import Link from "next/link";
import SocialRegister from "./_components/SocialRegister";
import Image from "next/image";

export default function Register() {
  return (
    <main className="w-full h-full min-h-screen flex justify-between">
      <div className="w-1/2 flex items-center justify-center">
        <div className="flex flex-col justify-between gap-12 max-w-md p-5">
          <h2 className="text-[32px] leading-[48px] font-medium">
            Get Started Now
          </h2>
          <RegisterForm />
          <p className="text-[10px] text-center">or</p>
          <SocialRegister />
          <p className="text-sm font-medium text-center">
            Have an account?{" "}
            <Link href="/login" className="text-blue-600">
              Sign in
            </Link>
          </p>
        </div>
      </div>
      <div className="w-1/2 min-h-screen relative">
        <Image
          src={"/Imgregisterbg.svg"}
          fill
          alt="register background"
          className="object-cover"
        />
      </div>
    </main>
  );
}
