import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Sparkles, ChevronRight, X, Play, Code2, Cpu } from 'lucide-react';

const steps = [
  {
    title: "Welcome to CodeFlow",
    content: "Visualize your code execution in real-time with AI-powered insights.",
    icon: <Sparkles className="w-8 h-8 text-accent" />,
  },
  {
    title: "Write & Debug",
    content: "The CodeEditor provides instant feedback and syntax highlighting for your logic.",
    icon: <Code2 className="w-8 h-8 text-sky-400" />,
  },
  {
    title: "Live Execution",
    content: "Press 'Run' or 'Step' to see the flow analyzer track every variable change.",
    icon: <Play className="w-8 h-8 text-success" />,
  },
  {
    title: "AI Explanation",
    content: "The AI system understands your code intent and explains the logic step-by-step.",
    icon: <Cpu className="w-8 h-8 text-purple-400" />,
  }
];

export default function OnboardingGuide() {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const hasSeenOnboarding = localStorage.getItem('hasSeenOnboarding');
    if (!hasSeenOnboarding) {
      setTimeout(() => setIsVisible(true), 1200);
    }
  }, []);

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      complete();
    }
  };

  const complete = () => {
    setIsVisible(false);
    localStorage.setItem('hasSeenOnboarding', 'true');
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[200] flex items-center justify-center p-6 bg-bg-primary/80 backdrop-blur-xl"
        >
          <motion.div 
            initial={{ scale: 0.9, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="w-full max-w-md p-8 rounded-3xl bg-bg-secondary border border-border/60 shadow-2xl relative overflow-hidden"
          >
            {/* Background Glow */}
            <div className="absolute -top-24 -right-24 w-48 h-48 bg-accent/10 rounded-full blur-[80px]" />
            <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-purple-500/10 rounded-full blur-[80px]" />

            <button 
              onClick={complete}
              className="absolute top-6 right-6 p-1.5 text-text-muted hover:text-text-primary transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex flex-col items-center text-center space-y-6">
              <motion.div
                key={currentStep}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="w-16 h-16 rounded-2xl bg-bg-panel border border-border flex items-center justify-center shadow-lg"
              >
                {steps[currentStep].icon}
              </motion.div>

              <div className="space-y-2">
                <h2 className="text-xl font-bold text-text-primary tracking-tight">
                  {steps[currentStep].title}
                </h2>
                <p className="text-sm text-text-muted leading-relaxed px-4">
                  {steps[currentStep].content}
                </p>
              </div>

              {/* Progress Dots */}
              <div className="flex gap-2">
                {steps.map((_, i) => (
                  <div 
                    key={i}
                    className={`h-1.5 rounded-full transition-all duration-300 ${
                      i === currentStep ? 'w-6 bg-accent' : 'w-1.5 bg-border'
                    }`}
                  />
                ))}
              </div>

              <button
                onClick={nextStep}
                className="w-full py-3.5 bg-accent hover:bg-accent-light text-white font-semibold rounded-xl tracking-tight transition-all active:scale-[0.98] flex items-center justify-center gap-2 group"
              >
                {currentStep === steps.length - 1 ? "Get Started" : "Continue"}
                <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
