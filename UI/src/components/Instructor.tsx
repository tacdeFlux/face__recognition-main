"use client"

import { WavyBackground } from "./ui/wavy-background";

const instructors = [
    {
      id: 1,
      name: 'Rupendra Mam',
      designation: 'Head of Project',
      image:
        'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60',
    },
    {
      id: 2,
      name: 'Anil Sir',
      designation: 'Project Mentor',
      image:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80',
    },
    {
      id: 3,
      name: 'gopal',
      designation: 'Team Leader',
      image:
        'https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60',
    },
    {
      id: 4,
      name: 'test',
      designation: 'Project Leader',
      image:
        'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60',
    },
  ];

const Instructor = () => {
  return (
    <div className="relative min-h-[50rem] flex flex-col items-center justify-center py-10 bg-slate-900">
      <h2 className="text-2xl md:text-4xl lg:text-5xl text-white font-bold text-center mb-8">
        Meet Our Instructors
      </h2>
      <p className="text-base md:text-lg text-gray-300 text-center mb-8 max-w-2xl">
        Instructors guide coders through programming concepts and best practices. Simple presentation with no hover effect.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-6xl px-4">
        {instructors.map((inst) => (
          <div
            key={inst.id}
            className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-4 text-center"
          >
            <img
              src={inst.image}
              alt={inst.name}
              className="mx-auto h-24 w-24 rounded-full object-cover mb-4"
            />
            <h3 className="text-white font-semibold text-lg">{inst.name}</h3>
            <p className="text-gray-300 text-sm">{inst.designation}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Instructor
