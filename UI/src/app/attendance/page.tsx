"use client";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { useAuth } from "@clerk/nextjs";
import React, { useEffect, useState } from "react";
import { MdAssignment } from "react-icons/md";
import { MdControlPointDuplicate } from "react-icons/md";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {useRouter} from 'next/navigation'
interface AttendancePageProps {
  mess?: string;
  l: number;
  names: string[];
  rolls: string[];
  times: string[];
  totalreg: number;
}

const AttendencePage: React.FC<AttendancePageProps> = ({
  mess,
  l,
  names,
  rolls,
  times,
  totalreg,
}) => {
  const [attendanceData, setAttendanceData] = useState({
    names: names || [],
    rolls: rolls || [],
    times: times || [],
    l: l || 0,
  });

  const [userCount, setUserCount] = useState(totalreg || 0);
  const [message, setMessage] = useState<string>("");
  const [addStatus, setAddStatus] = useState<string>("");
  const [isAdding, setIsAdding] = useState<boolean>(false);
  const { userId } = useAuth();
  const  router    = useRouter();
  // console.log(userId);

  const handleAttendence = () => {
    setMessage("Starting attendance... (camera should open on server machine)");
    fetch("http://127.0.0.1:8080/start")
      .then((response) => response.json())
      .then((data) => {
        if (data.mess) {
          setMessage(data.mess);
        } else {
          setMessage("Attendance recorded successfully.");
        }

        setAttendanceData({
          names: data.names,
          rolls: data.rolls,
          times: data.times,
          l: data.l,
        });
      })
      .catch((error) => {
        console.error("Error fetching attendance:", error);
        setMessage("Error contacting server for attendance. Check backend logs.");
      });
  };

  const handleStopAttendance = () => {
    setMessage("Stopping camera...");
    fetch("http://127.0.0.1:8080/stop")
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          setMessage(data.message);
        } else {
          setMessage("Camera stop requested.");
        }
      })
      .catch((error) => {
        console.error("Error stopping camera:", error);
        setMessage("Error sending stop command. Check backend logs.");
      });
  };

  const handleAddUser = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setIsAdding(true);
    setAddStatus("");

    try {
      const response = await fetch("http://127.0.0.1:8080/add", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (result.success) {
        const successText = result.message || "User added successfully.";
        setMessage(successText);
        setAddStatus(successText);
        setUserCount((prevCount) => prevCount + 1);
        router.refresh();
      } else {
        const failText = result.message || "Failed to add user.";
        setMessage(failText);
        setAddStatus(failText);
      }
    } catch (error) {
      console.error("Error adding user:", error);
      setMessage("Error adding user. Check console for details.");
      setAddStatus("Add new user");
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <>
      {userId ? (
        <div className="text-center">
          <h1 className="text-white p-3 text-4xl mt-[105px] md:mt-28 lg:mt-28">
            Face Recognition System of ADGIPS via HaarCascade and LBPH
          </h1>

          {message && <p className="text-yellow-300 text-lg mb-2">{message}</p>}
          {mess && <p className="text-red-500 text-xl">{mess}</p>}

          <div className="flex justify-center space-x-4 p-5 m-5 flex-col-reverse md:flex-row lg:flex-row">
            {/* leftSide  */}
            <div className="bg-black bg-opacity-80 rounded-lg p-0 m-2 min-h-[400px] flex flex-col gap-5 flex-1">
              <div className="flex items-center justify-center bg-white text-black rounded-md shadow-lg">
                <h2 className="p-2 font-bold">Today's Attendance</h2>
                <MdAssignment />
              </div>
              <div className="flex items-center justify-center gap-2 rounded-md shadow-lg bg-blue-600 text-white p-2">
                <button
                  className="bg-gradient-to-br relative group/btn from-black dark:from-zinc-900 dark:to-zinc-900 to-neutral-600 block dark:bg-zinc-800 text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset] px-4"
                  onClick={handleAttendence}
                >
                  Take Attendance
                </button>
                <button
                  className="bg-gradient-to-br relative group/btn from-black dark:from-zinc-900 dark:to-zinc-900 to-red-600 block dark:bg-zinc-800 text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset] px-4"
                  onClick={handleStopAttendance}
                >
                  Close Camera
                </button>
              </div>
              <table className="bg-white w-full text-black rounded-md">
                <thead>
                  <tr>
                    <th className="px-4 py-2">
                      <b>S.No</b>
                    </th>
                    <th className="px-4 py-2">
                      <b>Name</b>
                    </th>
                    <th className="px-4 py-2">
                      <b>ID</b>
                    </th>
                    <th className="px-4 py-2">
                      <b>Time</b>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {attendanceData.l > 0 &&
                    Array.from({ length: attendanceData.l }, (_, i) => (
                      <tr key={i}>
                        <td className="border px-4 py-2">{i + 1}</td>
                        <td className="border px-4 py-2">
                          {attendanceData.names[i]}
                        </td>
                        <td className="border px-4 py-2">
                          {attendanceData.rolls[i]}
                        </td>
                        <td className="border px-4 py-2">
                          {attendanceData.times[i]}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>

            {/* RightSide  */}
            <div className="bg-black bg-opacity-80 rounded-lg p-0 m-2 h-[400px] flex flex-col -mt-2 md:mt-2 lg:mt-2">
              <form onSubmit={handleAddUser}>
                <div className="flex items-center justify-center bg-white text-black rounded-md shadow-lg">
                  <h2 className="p-2 font-bold">Add New User</h2>
                  <MdControlPointDuplicate className="h-5 w-5 font-bold" />
                </div>
                <div className="flex items-center justify-center flex-col gap-4">
                  <div className="flex items-center justify-center gap-4 mt-5 flex-col md:flex-row lg:flex-row">
                    <Label htmlFor="newusername" className="text-white text-lg">
                      Enter New User Name*
                    </Label>
                    <Input
                      type="text"
                      id="newusername"
                      name="newusername"
                      className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                      required
                    />
                  </div>
                  <div className="flex justify-center items-center gap-4 flex-col md:flex-row lg:flex-row">
                    <Label htmlFor="newuserid" className="text-white text-lg">
                      Enter New User ID NO*
                    </Label>
                    <Input
                      type="number"
                      id="newuserid"
                      name="newuserid"
                      className="text-black p-2 rounded-md shadow-md ring-1 outline-none bg-slate-300 md:w-60 lg:w-60 w-72"
                      required
                    />
                  </div>
                </div>

                <button
                  className="bg-gradient-to-br relative group/btn from-black dark:from-zinc-900 dark:to-zinc-900 to-neutral-600 block dark:bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset] md:mt-12 lg:mt-12 mt-10"
                  type="submit"
                  disabled={isAdding}
                >
                  {isAdding
                    ? "Adding..."
                    : addStatus
                    ? addStatus
                    : "Add New User →"}
                </button>
              </form>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-4 relative z-10 text-center flex justify-center items-center h-screen w-full">
          <BackgroundBeams />
          <h1 className="mt-20 md:mt-0 text-4xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400">
            Face Recognition Login Required for Attendance
          </h1>
        </div>
      )}
    </>
  );
};

export default AttendencePage;
