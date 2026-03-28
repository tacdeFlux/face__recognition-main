import ChooseUs from "@/components/ChooseUs";
import Featured from "@/components/Featured";
import Footer from "@/components/Footer";
import HeroSection from "@/components/HeroSection";
import Instructor from "@/components/Instructor";
import TestimonialCards from "@/components/TestimonialCards";
import UpcommingWebinars from "@/components/UpcommingWebinars";
import { SolarSystem } from "@/components/ui/solar-system";

export default function Home() {
  return (
    <main className="min-h-screen bg-black/[0.96] antialiased bg-grid-white/[0.02] scrollbar-hide relative overflow-hidden">
      <SolarSystem />
      <div className="relative z-10">
      <HeroSection />
      <div className="border-t border-neutral-800/50"/>
      <Featured />
      <div className="border-t border-neutral-800/50"/>
      <ChooseUs />
      <div className="border-t border-neutral-800/50"/>
      <TestimonialCards />
      <div className="border-t border-neutral-800/50"/>
      <UpcommingWebinars />
      <div className="border-t border-neutral-800/50"/>
      <Instructor />
      <Footer />
      </div>
    </main>
  );
}
