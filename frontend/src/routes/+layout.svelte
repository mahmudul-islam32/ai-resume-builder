<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/auth';

  import '../app.css';
  
  let showMobileMenu = false;
  
  onMount(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (token) {
      // Validate token and set user
      // This would typically make an API call to verify the token
    }
  });
  
  function logout(): void {
    localStorage.removeItem('token');
    user.set(null);
    goto('/login');
  }
  
  function toggleMobileMenu(): void {
    showMobileMenu = !showMobileMenu;
  }
</script>

<div class="min-h-screen bg-gray-50">
  {#if $user}
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <a href="/dashboard" class="text-2xl font-bold text-primary-600">
                AI Resume
              </a>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <a href="/dashboard" class="border-primary-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Dashboard
              </a>
              <a href="/resumes" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Resumes
              </a>
              <a href="/applications" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Applications
              </a>
              <a href="/interviews" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Interviews
              </a>
            </div>
          </div>
          
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
            <div class="ml-3 relative">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-700">
                  {$user?.first_name} {$user?.last_name}
                </span>
                <button
                  on:click={logout}
                  class="btn btn-outline text-sm"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
          
          <!-- Mobile menu button -->
          <div class="sm:hidden flex items-center">
            <button
              on:click={toggleMobileMenu}
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      {#if showMobileMenu}
        <div class="sm:hidden">
          <div class="pt-2 pb-3 space-y-1">
            <a href="/dashboard" class="bg-primary-50 border-primary-500 text-primary-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Dashboard
            </a>
            <a href="/resumes" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Resumes
            </a>
            <a href="/applications" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Applications
            </a>
            <a href="/interviews" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Interviews
            </a>
          </div>
          <div class="pt-4 pb-3 border-t border-gray-200">
            <div class="flex items-center px-4">
              <div class="flex-shrink-0">
                <span class="text-sm font-medium text-gray-800">
                  {$user?.first_name} {$user?.last_name}
                </span>
              </div>
            </div>
            <div class="mt-3 space-y-1">
              <button
                on:click={logout}
                class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      {/if}
    </nav>
  {/if}
  
  <!-- Main content -->
  <main class="{$user ? 'max-w-7xl mx-auto py-6 sm:px-6 lg:px-8' : ''}">
    <slot />
  </main>
</div>
