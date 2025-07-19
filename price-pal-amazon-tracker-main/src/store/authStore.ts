
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { auth } from '@/lib/firebase';
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  updateProfile,
  User as FirebaseUser,
} from 'firebase/auth';

interface User {
  uid: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loginWithEmail: (email: string, password: string) => Promise<void>;
  signupWithEmail: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  sendPasswordReset: (email: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      loginWithEmail: async (email, password) => {
        const cred = await signInWithEmailAndPassword(auth, email, password);
        const firebaseUser = cred.user;
        const token = await firebaseUser.getIdToken();
        set({
          user: {
            uid: firebaseUser.uid,
            name: firebaseUser.displayName || '',
            email: firebaseUser.email || '',
          },
          token,
          isAuthenticated: true,
        });
      },
      signupWithEmail: async (name, email, password) => {
  const cred = await createUserWithEmailAndPassword(auth, email, password);
  await updateProfile(cred.user, { displayName: name });
  const token = await cred.user.getIdToken();

  const metadata = cred.user.metadata;
  const isNewUser = metadata.creationTime === metadata.lastSignInTime;

  set({
    user: {
      uid: cred.user.uid,
      name,
      email: cred.user.email || '',
    },
    token,
    isAuthenticated: true,
  });

  // ✅ Only trigger welcome email if it's a new user
  if (isNewUser) {
    try {
      const res = await fetch("http://localhost:8000/auth/send-login-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name }),
      });

      const data = await res.json();
      console.log("Email send response:", data);

      if (!res.ok) {
        throw new Error(data.detail || "Email send failed");
      }
    } catch (err) {
      console.error("Failed to send welcome email:", err);
    }
  }
},

      logout: async () => {
        await signOut(auth);
        set({ user: null, token: null, isAuthenticated: false });
      },
      sendPasswordReset: async (email) => {
        try {
          await sendPasswordResetEmail(auth, email);
          console.log('Password reset email sent successfully');
        } catch (error) {
          throw new Error(error.message || 'Failed to send password reset email');
        }
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
