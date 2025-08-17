<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/auth';
  import type { Resume } from '$lib/types/dashboard';
  import { DateUtils } from '$lib/utils/date';
  
  let resumes: Resume[] = [];
  let loading = true;
  let error: string | null = null;
  
  onMount(async () => {
    if (!$user) {
      goto('/login');
      return;
    }
    
    await loadResumes();
  });
  
  async function loadResumes(): Promise<void> {
    try {
      loading = true;
      error = null;
      
      // Mock data for now
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      resumes = [
        {
          id: '1',
          title: 'Senior Frontend Developer Resume',
          created_at: '2024-01-10T10:00:00Z',
          updated_at: '2024-01-15T14:30:00Z',
          is_active: true,
          file_path: '/uploads/resume_1.pdf'
        },
        {
          id: '2',
          title: 'Full Stack Engineer Resume',
          created_at: '2024-01-08T09:00:00Z',
          updated_at: '2024-01-12T16:45:00Z',
          is_active: false,
          file_path: '/uploads/resume_2.pdf'
        },
        {
          id: '3',
          title: 'React Developer Resume',
          created_at: '2024-01-05T11:20:00Z',
          updated_at: '2024-01-11T12:15:00Z',
          is_active: false,
          file_path: '/uploads/resume_3.pdf'
        }
      ];
    } catch (err) {
      error = 'Failed to load resumes';
      console.error('Error loading resumes:', err);
    } finally {
      loading = false;
    }
  }
  
  function handleEdit(resumeId: string): void {
    goto(`/resumes/${resumeId}/edit`);
  }
  
  function handleDownload(resume: Resume): void {
    if (resume.file_path) {
      window.open(resume.file_path, '_blank');
    }
  }
  
  function handleSetActive(resumeId: string): void {
    resumes = resumes.map(resume => ({
      ...resume,
      is_active: resume.id === resumeId
    }));
  }
  
  async function handleDelete(resumeId: string): Promise<void> {
    if (!confirm('Are you sure you want to delete this resume?')) {
      return;
    }
    
    try {
      // API call would go here
      resumes = resumes.filter(resume => resume.id !== resumeId);
    } catch (err) {
      error = 'Failed to delete resume';
    }
  }
</script>

<svelte:head>
  <title>My Resumes - AI Resume Builder</title>
</svelte:head>

<div class="px-4 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="sm:flex sm:items-center">
    <div class="sm:flex-auto">
      <h1 class="text-3xl font-bold text-gray-900">My Resumes</h1>
      <p class="mt-2 text-gray-700">
        Manage your resume collection and create new ones tailored to specific job applications.
      </p>
    </div>
    <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
      <a href="/resumes/new" class="btn btn-primary">
        Create New Resume
      </a>
    </div>
  </div>

  {#if error}
    <div class="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="ml-3">
          <p class="text-sm text-red-800">{error}</p>
        </div>
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="mt-8 flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <span class="ml-3 text-gray-600">Loading resumes...</span>
    </div>
  {:else if resumes.length === 0}
    <div class="mt-8 text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No resumes</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating your first resume.</p>
      <div class="mt-6">
        <a href="/resumes/new" class="btn btn-primary">
          Create New Resume
        </a>
      </div>
    </div>
  {:else}
    <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {#each resumes as resume}
        <div class="relative bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
          {#if resume.is_active}
            <div class="absolute top-4 right-4">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Active
              </span>
            </div>
          {/if}
          
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4 flex-1">
              <h3 class="text-lg font-medium text-gray-900 truncate">
                {resume.title}
              </h3>
            </div>
          </div>
          
          <div class="mt-4">
            <p class="text-sm text-gray-600">
              Created: {DateUtils.formatDate(resume.created_at)}
            </p>
            <p class="text-sm text-gray-600">
              Updated: {DateUtils.formatDate(resume.updated_at)}
            </p>
          </div>
          
          <div class="mt-6 flex items-center justify-between">
            <div class="flex space-x-2">
              <button
                on:click={() => handleEdit(resume.id)}
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Edit
              </button>
              <button
                on:click={() => handleDownload(resume)}
                class="text-gray-600 hover:text-gray-700 text-sm font-medium"
              >
                Download
              </button>
            </div>
            
            <div class="flex items-center space-x-2">
              {#if !resume.is_active}
                <button
                  on:click={() => handleSetActive(resume.id)}
                  class="text-green-600 hover:text-green-700 text-sm font-medium"
                >
                  Set Active
                </button>
              {/if}
              <button
                on:click={() => handleDelete(resume.id)}
                class="text-red-600 hover:text-red-700 text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
