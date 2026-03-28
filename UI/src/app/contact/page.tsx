"use client";
import { useState } from "react";
import React, { useRef } from "react";
import emailjs from "@emailjs/browser";
import { useAuth } from "@clerk/nextjs";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { BackgroundLines } from "@/components/ui/background-lines";

export default function Contact() {
  const [newusername, setNewUsername] = useState("");
  const [newuserid, setNewUserid] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const form = useRef<HTMLFormElement>(null);
  const { userId } = useAuth();

  const sendEmail = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    emailjs
      .sendForm("service_b1bg27e", "template_ce0wi2i", form.current!, {
        publicKey: "DaiGbhHqN3GlsEBTt",
      })
      .then(
        () => {
          console.log("SUCCESS!");
        },

        (error) => {
          console.log("FAILED...", error.text);
        }
      );
    setNewUsername("");
    setNewUserid("");
    setSubject("");
    setMessage("");
  };

  return (
    <>
      {userId ? (
        <div className="bg-black bg-opacity-80 rounded-lg p-0 m-2 h-[400px] flex flex-col -mt-2 md:mt-2 lg:mt-2 items-center justify-center">
          <form ref={form} onSubmit={sendEmail}>
            <div className="flex items-center justify-center flex-col gap-4 md:mt-40 lg:mt-40 mt-[350px]">
              <div className="flex items-center justify-center gap-4 mt-5 flex-col md:flex-row lg:flex-row">
                <Label htmlFor="newuserid" className="text-white text-lg">
                  Enter User Name*
                </Label>
                <Input
                  type="text"
                  placeholder="Your Name"
                  value={newusername}
                  id="newusername"
                  name="name"
                  onChange={(e) => setNewUsername(e.target.value)}
                  className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                  required
                />
              </div>
              <div className="flex justify-center items-center gap-4 flex-col md:flex-row lg:flex-row">
                <Label className="text-white text-lg">Enter User ID NO*</Label>
                <Input
                  type="number"
                  id="newuserid"
                  name="userid"
                  placeholder="Your ID"
                  value={newuserid}
                  onChange={(e) => setNewUserid(e.target.value)}
                  className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                  required
                />
              </div>
              <div className="flex justify-center items-center gap-3 flex-col md:flex-row lg:flex-row">
                <Label className="text-white text-lg">
                  Enter Subject.......*
                </Label>
                <Input
                  type="text"
                  placeholder="Subject"
                  value={subject}
                  id="newuserid"
                  name="subject"
                  onChange={(e) => setSubject(e.target.value)}
                  className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                  required
                />
              </div>
              <div className="flex justify-center items-center gap-3 flex-col md:flex-row lg:flex-row">
                <Label className="text-white text-lg">Enter Message....*</Label>
                <Input
                  placeholder="Message"
                  value={message}
                  id="newuserid"
                  name="message"
                  onChange={(e) => setMessage(e.target.value)}
                  className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                  required
                />
              </div>
            </div>
            <button
              type="submit"
              className="bg-gradient-to-br relative group/btn from-black dark:from-zinc-900 dark:to-zinc-900 to-neutral-600 block dark:bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset] md:mt-12 lg:mt-12 mt-10"
            >
              Send Email
            </button>
          </form>
        </div>
      ) : (
        <BackgroundLines className="flex items-center justify-center w-full flex-col px-4">
          <div className="p-4 relative z-10 text-center flex justify-center items-center h-screen w-full">
            <h1 className="mt-20 md:mt-0 text-4xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400">
              Get the Support You Need - Login to Connect with Mentors
            </h1>
          </div>
        </BackgroundLines>
      )}
    </>
  );
}
