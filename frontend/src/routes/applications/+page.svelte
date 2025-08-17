<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/auth';
  import type { Application } from '$lib/types/dashboard';
  import { DateUtils } from '$lib/utils/date';
  
  let applications: Application[] = [];
  let loading = true;
  let error: string | null = null;
  let selectedStatus: string = 'all';
  
  const statusOptions = [
    { value: 'all', label: 'All Applications' },
    { value: 'applied', label: 'Applied' },
    { value: 'interview', label: 'Interview' },
    { value: 'offer', label: 'Offer' },
    { value: 'rejected', label: 'Rejected' }
  ];
  
  onMount(async () => {
    if (!$user) {
      goto('/login');
      return;
    }
    
    await loadApplications();
  });
  
  async function loadApplications(): Promise<void> {
    try {
      loading = true;
      error = null;
      
      // Mock data for now
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      applications = [
        {
          id: '1',
          company_name: 'TechCorp Inc.',
          job_title: 'Senior Frontend Developer',
          status: 'interview',
          applied_date: '2024-01-15',
          salary_range: '$90k - $120k',
          location: 'San Francisco, CA'
        },
        {
          id: '2',
          company_name: 'StartupXYZ',
          job_title: 'Full Stack Engineer',
          status: 'applied',
          applied_date: '2024-01-14',
          salary_range: '$80k - $110k',
          location: 'Remote'
        },
        {
          id: '3',
          company_name: 'BigTech Solutions',
          job_title: 'React Developer',
          status: 'rejected',
          applied_date: '2024-01-12',
          salary_range: '$85k - $115k',
          location: 'New York, NY'
        },
        {
          id: '4',
          company_name: 'Innovation Labs',
          job_title: 'UI/UX Developer',
          status: 'offer',
          applied_date: '2024-01-10',
          salary_range: '$95k - $125k',
          location: 'Austin, TX'
        },
        {
          id: '5',
          company_name: 'CloudTech Corp',
          job_title: 'Frontend Engineer',
          status: 'applied',
          applied_date: '2024-01-08',
          salary_range: '$75k - $105k',
          location: 'Seattle, WA'
        }
      ];
    } catch (err) {
      error = 'Failed to load applications';
      console.error('Error loading applications:', err);
    } finally {
      loading = false;
    }
  }
  
  function getStatusColor(status: string): string {
    switch (status) {
      case 'applied': return 'bg-blue-100 text-blue-800';
      case 'interview': return 'bg-yellow-100 text-yellow-800';
      case 'offer': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }
  
  function handleEdit(applicationId: string): void {
    goto(`/applications/${applicationId}/edit`);
  }
  
  async function handleDelete(applicationId: string): Promise<void> {
    if (!confirm('Are you sure you want to delete this application?')) {
      return;
    }
    
    try {
      applications = applications.filter(app => app.id !== applicationId);
    } catch (err) {
      error = 'Failed to delete application';
    }
  }
  
  $: filteredApplications = selectedStatus === 'all' 
    ? applications 
    : applications.filter(app => app.status === selectedStatus);
</script>

<svelte:head>
  <title>Applications - AI Resume Builder</title>
</svelte:head>

<div class="px-4 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="sm:flex sm:items-center">
    <div class="sm:flex-auto">
      <h1 class="text-3xl font-bold text-gray-900">Job Applications</h1>
      <p class="mt-2 text-gray-700">
        Track and manage all your job applications in one place.
      </p>
    </div>
    <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
      <a href="/applications/new" class="btn btn-primary">
        Add Application
      </a>
    </div>
  </div>

  <!-- Filters -->
  <div class="mt-6">
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <label for="status-filter" class="block text-sm font-medium text-gray-700">
          Filter by status
        </label>
        <select
          id="status-filter"
          bind:value={selectedStatus}
          class="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-primary-500 focus:outline-none focus:ring-primary-500 sm:text-sm"
        >
          {#each statusOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
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
      <span class="ml-3 text-gray-600">Loading applications...</span>
    </div>
  {:else if filteredApplications.length === 0}
    <div class="mt-8 text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No applications found</h3>
      <p class="mt-1 text-sm text-gray-500">
        {selectedStatus === 'all' ? 'Get started by tracking your first job application.' : `No applications with status "${selectedStatus}".`}
      </p>
      <div class="mt-6">
        <a href="/applications/new" class="btn btn-primary">
          Add Application
        </a>
      </div>
    </div>
  {:else}
    <!-- Applications Table -->
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                    Company & Position
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Status
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Applied Date
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Salary Range
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Location
                  </th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                    <span class="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white">
                {#each filteredApplications as application}
                  <tr class="hover:bg-gray-50">
                    <td class="whitespace-nowrap py-4 pl-4 pr-3 sm:pl-6">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{application.job_title}</div>
                        <div class="text-sm text-gray-500">{application.company_name}</div>
                      </div>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      <span class="inline-flex rounded-full px-2 text-xs font-semibold leading-5 {getStatusColor(application.status)}">
                        {application.status}
                      </span>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      {DateUtils.formatDate(application.applied_date)}
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      {application.salary_range || 'Not specified'}
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                      {application.location || 'Not specified'}
                    </td>
                    <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                      <button
                        on:click={() => handleEdit(application.id)}
                        class="text-primary-600 hover:text-primary-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        on:click={() => handleDelete(application.id)}
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
