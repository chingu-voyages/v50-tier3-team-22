"use client";
import Image from "next/image";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

export default function UploadImage({ register, setValue }: any) {
  const [file, setFile] = useState<string | null>(null);
  const fileTypes = ["JPG", "PNG", "GIF"];
  const handleChange = async (file: File) => {
    setFile(URL.createObjectURL(file));
    const formData = new FormData();
    const url = "https://api.cloudinary.com/v1_1/daio3ee4e/upload";
    formData.append("file", file);
    formData.append("upload_preset", "bgfig1pg");

    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      console.log("response", response);
      const data = await response.json();
      setFile(data.secure_url);
      register("image");
      setValue("image", data.secure_url);
      console.log("data", data);
    }
  };

  console.log({ file });

  function DropZone() {
    return file ? (
      <div className="w-full h-full relative rounded">
        <Image
          src={file}
          alt="upload image placeholder"
          fill
          className="cursor-pointer object-cover rounded"
        />
      </div>
    ) : (
      <div className="w-full h-full rounded border bg-[#EFEFEF] cursor-pointer flex justify-center items-center">
        <Image
          src={"/svg/uploadPlaceHolder.svg"}
          alt="upload image placeholder"
          width={64}
          height={68}
        />
      </div>
    );
  }

  return (
    <FileUploader
      handleChange={handleChange}
      name="file"
      types={fileTypes}
      children={<DropZone></DropZone>}
    />
  );
}
