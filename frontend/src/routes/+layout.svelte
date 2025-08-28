<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { user, checkAuth, logout } from '$lib/stores/auth';

  import '../app.css';
  
  let showMobileMenu = false;
  let isCheckingAuth = true;
  let authCheckComplete = false;
  
  // Define protected routes that require authentication
  const protectedRoutes = ['/dashboard', '/resumes', '/applications', '/interviews', '/match', '/cover-letters'];
  
  // Check if current route is protected
  $: isProtectedRoute = protectedRoutes.some(route => $page.url.pathname.startsWith(route));
  
  onMount(async () => {
    console.log('🔍 Layout mounted - checking route:', $page.url.pathname);
    console.log('🔍 Is protected route:', isProtectedRoute);
    
    if (isProtectedRoute) {
      console.log('🔍 Protected route detected - checking authentication...');
      
      try {
        // Check if user is authenticated
        console.log('🔍 Calling checkAuth()...');
        const isAuthenticated = await checkAuth();
        console.log('🔍 checkAuth() result:', isAuthenticated);
        
        if (!isAuthenticated) {
          console.log('🔍 User not authenticated, redirecting to login...');
          // Redirect to login if not authenticated
          goto('/login');
          return; // Exit early to prevent further processing
        } else {
          console.log('🔍 User is authenticated, staying on current page');
        }
      } catch (error) {
        console.error('🔍 Authentication check failed:', error);
        // If authentication check fails, redirect to login
        goto('/login');
        return; // Exit early to prevent further processing
      }
    } else {
      console.log('🔍 Public route - no authentication required');
    }
    
    console.log('🔍 Authentication check completed, setting isCheckingAuth = false');
    isCheckingAuth = false;
    authCheckComplete = true;
  });
  
  function handleLogout(): void {
    console.log('🔍 Logout clicked');
    logout();
  }
  
  function toggleMobileMenu(): void {
    showMobileMenu = !showMobileMenu;
  }
</script>

{#if isCheckingAuth && isProtectedRoute}
  <!-- Loading screen while checking authentication for protected routes -->
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Checking authentication...</p>
      <p class="text-sm text-gray-500">Please wait while we verify your session</p>
    </div>
  </div>
{:else if $user && isProtectedRoute}
  <div class="min-h-screen bg-gray-50">
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
              <a href="/match" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Match
              </a>
              <a href="/cover-letters" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Cover Letters
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
                  on:click={handleLogout}
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
            <a href="/match" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Match
            </a>
            <a href="/cover-letters" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">
              Cover Letters
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
                on:click={handleLogout}
                class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      {/if}
    </nav>
    
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <slot />
    </main>
  </div>
{:else if isProtectedRoute && authCheckComplete && !$user}
  <!-- User tried to access protected route but is not authenticated -->
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <div class="text-red-500 mb-4">
        <svg class="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">Authentication Required</h3>
      <p class="text-gray-600 mb-4">You need to be logged in to access this page.</p>
      <a href="/login" class="btn btn-primary">
        Go to Login
      </a>
    </div>
  </div>
{:else}
  <!-- Public routes or not authenticated - show content without navigation -->
  <main>
    <slot />
  </main>
{/if}
