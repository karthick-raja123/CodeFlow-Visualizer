import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, X, Loader2 } from 'lucide-react';

export function LoadingOverlay({ message = "Processing..." }) {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-bg-primary/60 backdrop-blur-sm"
    >
      <div className="flex flex-col items-center gap-3 p-6 rounded-2xl bg-bg-secondary border border-border shadow-2xl">
        <Loader2 className="w-8 h-8 text-accent animate-spin" />
        <p className="text-sm font-medium text-text-primary tracking-tight">{message}</p>
      </div>
    </motion.div>
  );
}

export function ErrorToast({ error, onClose }) {
  if (!error) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] min-w-[320px] max-w-md p-4 flex items-start gap-3 bg-red-500/10 border border-red-500/20 backdrop-blur-md rounded-xl shadow-xl shadow-red-500/5"
    >
      <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
      <div className="flex-1">
        <p className="text-sm font-semibold text-red-500">Execution Error</p>
        <p className="text-xs text-red-400/90 leading-relaxed mt-1">{error}</p>
      </div>
      <button 
        onClick={onClose}
        className="p-1 hover:bg-white/10 rounded-md transition-colors"
      >
        <X className="w-4 h-4 text-red-400" />
      </button>
    </motion.div>
  );
}
