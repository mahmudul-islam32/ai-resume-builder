<script lang="ts">
  import { goto } from '$app/navigation';
  import { user, isLoading, error } from '$lib/stores/auth';
  import api from '$lib/utils/api';
  import type { AxiosError } from 'axios';

  let email: string = '';
  let password: string = '';
  let confirmPassword: string = '';
  let firstName: string = '';
  let lastName: string = '';

  async function handleRegister(): Promise<void> {
    if (!email || !password || !confirmPassword || !firstName || !lastName) {
      error.set('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      error.set('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      error.set('Password must be at least 6 characters long');
      return;
    }

    isLoading.set(true);
    error.set(null);

    try {
      console.log('🔍 Attempting registration...');
      await api.post('/auth/register', {
        email,
        password,
        first_name: firstName,
        last_name: lastName
      });

      console.log('✅ Registration successful, auto-login...');
      // Auto-login after registration
      const loginResponse = await api.post('/auth/login', {
        email,
        password
      });

      console.log('✅ Auto-login successful:', loginResponse.data);
      // Set user data from the response
      user.set(loginResponse.data.user);

      goto('/dashboard');
    } catch (err: any) {
      console.error('❌ Registration failed:', err);
      const axiosError = err as AxiosError<{ detail: string }>;
      error.set(axiosError.response?.data?.detail || 'Registration failed');
    } finally {
      isLoading.set(false);
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <a href="/login" class="font-medium text-primary-600 hover:text-primary-500">
          sign in to your existing account
        </a>
      </p>
    </div>
    
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleRegister}>
      {#if $error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {$error}
        </div>
      {/if}
      
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="firstName" class="label">First name</label>
            <input
              id="firstName"
              name="firstName"
              type="text"
              required
              class="input"
              bind:value={firstName}
              placeholder="First name"
            />
          </div>
          
          <div>
            <label for="lastName" class="label">Last name</label>
            <input
              id="lastName"
              name="lastName"
              type="text"
              required
              class="input"
              bind:value={lastName}
              placeholder="Last name"
            />
          </div>
        </div>
        
        <div>
          <label for="email" class="label">Email address</label>
          <input
            id="email"
            name="email"
            type="email"
            autocomplete="email"
            required
            class="input"
            bind:value={email}
            placeholder="Enter your email"
          />
        </div>
        
        <div>
          <label for="password" class="label">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autocomplete="new-password"
            required
            class="input"
            bind:value={password}
            placeholder="Enter your password"
          />
        </div>
        
        <div>
          <label for="confirmPassword" class="label">Confirm password</label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            autocomplete="new-password"
            required
            class="input"
            bind:value={confirmPassword}
            placeholder="Confirm your password"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          class="btn btn-primary w-full"
          disabled={$isLoading}
        >
          {#if $isLoading}
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Creating account...
          {:else}
            Create account
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
