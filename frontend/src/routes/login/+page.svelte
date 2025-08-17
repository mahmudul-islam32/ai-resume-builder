<script lang="ts">
  import { goto } from '$app/navigation';
  import { user, isLoading, error } from '$lib/stores/auth';
  import api from '$lib/utils/api';
  import type { AxiosError } from 'axios';

  let email: string = '';
  let password: string = '';

  async function handleLogin(): Promise<void> {
    if (!email || !password) {
      error.set('Please fill in all fields');
      return;
    }

    isLoading.set(true);
    error.set(null);

    try {
      const response = await api.post('/auth/login', {
        email,
        password
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);

      // Get user info
      const userResponse = await api.get('/auth/me');
      user.set(userResponse.data);

      goto('/dashboard');
    } catch (err: any) {
      const axiosError = err as AxiosError<{ detail: string }>;
      error.set(axiosError.response?.data?.detail || 'Login failed');
    } finally {
      isLoading.set(false);
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Sign in to your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <a href="/register" class="font-medium text-primary-600 hover:text-primary-500">
          create a new account
        </a>
      </p>
    </div>
    
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
      {#if $error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {$error}
        </div>
      {/if}
      
      <div class="space-y-4">
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
            autocomplete="current-password"
            required
            class="input"
            bind:value={password}
            placeholder="Enter your password"
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
            Signing in...
          {:else}
            Sign in
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
