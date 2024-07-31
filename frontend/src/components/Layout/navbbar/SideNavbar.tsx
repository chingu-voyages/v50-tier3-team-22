import {
  BookmarkIcon,
  CalendarIcon,
  ClipboardIcon,
  HomeIcon,
  ReaderIcon,
} from "@radix-ui/react-icons";
import Link from "next/link";
import React from "react";

export default function SideNavbar() {
  return (
    <nav className="flex flex-col items-start px-2 text-sm font-medium gap-9 ">
      <Link
        href="#"
        className="flex items-center justify-start gap-2 h-10 w-full rounded-sm px-3 py-2  transition-all hover:bg-[#E4F0DB] hover:text-primary"
      >
        <HomeIcon />
        Home
      </Link>
      <Link
        href="#"
        className="flex items-center justify-start gap-2 h-10 w-full rounded-sm px-3 py-2  transition-all hover:bg-[#E4F0DB] hover:text-primary bg-primary-foreground"
      >
        <ReaderIcon />
        Recipes
      </Link>
      <Link
        href="#"
        className="flex items-center justify-start gap-2 h-10 w-full rounded-sm px-3 py-2  transition-all hover:bg-[#E4F0DB] hover:text-primary"
      >
        <ClipboardIcon />
        Shopping List
      </Link>
      <Link
        href="#"
        className="flex items-center justify-start gap-2 h-10 w-full rounded-sm px-3 py-2  transition-all hover:bg-[#E4F0DB] hover:text-primary"
      >
        <CalendarIcon />
        Meal Planner
      </Link>
      <Link
        href="#"
        className="flex items-center justify-start gap-2 h-10 w-full rounded-sm px-3 py-2  transition-all hover:bg-[#E4F0DB] hover:text-primary"
      >
        <BookmarkIcon />
        Favorites
      </Link>
    </nav>
  );
}
