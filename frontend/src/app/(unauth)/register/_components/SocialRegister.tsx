import Link from "next/link";
import React from "react";
import { FcGoogle } from "react-icons/fc";
import { FaApple, FaFacebook } from "react-icons/fa";

export default function SocialRegister() {
  return (
    <div className="flex gap-4 flex-wrap justify-around">
      <Link
        href={"/comming-soon"}
        className="bg-white text-black border-[#D9D9D9] border text-xs py-1 px-5 rounded-sm flex items-center gap-2 max-w-48"
      >
        <FcGoogle size={24} />
        Sign in with Google
      </Link>
      <Link
        href={"/comming-soon"}
        className="bg-white text-black border-[#D9D9D9] border text-xs py-1 px-5 rounded-sm flex items-center gap-2"
      >
        <FaApple size={24} />
        Sign in with Apple
      </Link>
      <Link
        href={"/comming-soon"}
        className="bg-white text-black border-[#D9D9D9] border text-xs py-1 px-5 rounded-sm flex items-center gap-2"
      >
        <FaFacebook color="#1877F2" size={24} />
        Sign in with Facebook
      </Link>
    </div>
  );
}
