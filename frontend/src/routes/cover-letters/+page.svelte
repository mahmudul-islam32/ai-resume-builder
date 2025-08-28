<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  import { 
    generateCoverLetter, 
    generateCustomizedCoverLetter,
    getCoverLetterTemplates,
    saveCoverLetterToLocalStorage,
    getSavedCoverLetters,
    deleteSavedCoverLetter,
    type CoverLetterTemplate,
    type CoverLetterCustomization
  } from '$lib/services/coverLetterService';

  // Types
  interface Resume {
    id: number;
    title: string;
    parsed_content: string;
  }

  interface JobPosting {
    id: number;
    title: string;
    company: string;
    description: string;
  }

  interface SavedLetter {
    id: number;
    content: string;
    metadata: {
      resume: string;
      job: string;
      company: string;
      generated_at: string;
    };
    created_at: string;
  }

  // State
  let resumes: Resume[] = [];
  let jobPostings: JobPosting[] = [];
  let selectedResume: Resume | null = null;
  let selectedJob: JobPosting | null = null;
  let coverLetterContent = '';
  let loading = false;
  let error: string | null = null;
  let success: string | null = null;
  let showCustomization = false;
  let savedLetters: SavedLetter[] = [];
  let templates: CoverLetterTemplate[] = [];
  let selectedTemplate: CoverLetterTemplate | null = null;
  let ollamaStatus = 'checking'; // 'checking', 'available', 'unavailable'

  // Form data
  let formData = {
    companyName: '',
    jobTitle: '',
    personalMessage: '',
    tone: 'professional' as const,
    focusAreas: [] as string[],
    customInstructions: '',
    includeSalary: false,
    includeAvailability: false,
    includePortfolio: false
  };

  // Job input method
  let jobInputMethod = 'select'; // 'select' or 'manual'
  let manualJobTitle = '';
  let manualJobCompany = '';
  let manualJobDescription = '';

  // Focus area options
  const focusAreaOptions = [
    'Technical Skills',
    'Leadership Experience',
    'Project Management',
    'Problem Solving',
    'Communication Skills',
    'Team Collaboration',
    'Innovation & Creativity',
    'Industry Knowledge',
    'Quantifiable Achievements',
    'Cultural Fit'
  ];

  const toneOptions = [
    { value: 'professional', label: 'Professional', description: 'Formal and business-like' },
    { value: 'friendly', label: 'Friendly', description: 'Warm and approachable' },
    { value: 'enthusiastic', label: 'Enthusiastic', description: 'Energetic and passionate' },
    { value: 'formal', label: 'Formal', description: 'Very traditional and conservative' }
  ];

  onMount(async () => {
    await loadInitialData();
    await checkOllamaStatus();
  });

  async function checkOllamaStatus() {
    try {
      // Check if Ollama is available by calling the available models endpoint
      const response = await fetch('/api/v1/ai/available-models');
      if (response.ok) {
        const data = await response.json();
        if (data.current_model === 'ollama') {
          ollamaStatus = 'available';
        } else {
          ollamaStatus = 'unavailable';
        }
      } else {
        ollamaStatus = 'unavailable';
      }
    } catch (error) {
      console.error('Failed to check Ollama status:', error);
      ollamaStatus = 'unavailable';
    }
  }

  async function loadInitialData() {
    try {
      // Load templates
      templates = await getCoverLetterTemplates();
      
      // Load saved letters
      savedLetters = getSavedCoverLetters();
      
      // Load real data from API
      await loadResumes();
      await loadJobPostings();
      
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  }

  async function loadResumes() {
    try {
      const response = await fetch('/api/v1/resumes');
      if (response.ok) {
        const data = await response.json();
        resumes = data.map((resume: any) => ({
          id: resume.id,
          title: resume.title || `Resume ${resume.id}`,
          parsed_content: resume.parsed_content || resume.content || 'No content available'
        }));
      } else {
        console.warn('Failed to load resumes, using fallback data');
        // Fallback data if API fails
        resumes = [
          { id: 1, title: 'My Resume', parsed_content: 'Please upload your resume to get started...' }
        ];
      }
    } catch (err) {
      console.error('Failed to load resumes:', err);
      // Fallback data
      resumes = [
        { id: 1, title: 'My Resume', parsed_content: 'Please upload your resume to get started...' }
      ];
    }
  }

  async function loadJobPostings() {
    try {
      const response = await fetch('/api/v1/jobs');
      if (response.ok) {
        const data = await response.json();
        jobPostings = data.map((job: any) => ({
          id: job.id,
          title: job.title || `Job ${job.id}`,
          company: job.company || 'Unknown Company',
          description: job.description || 'No description available'
        }));
      } else {
        console.warn('Failed to load job postings, using fallback data');
        // Fallback data if API fails
        jobPostings = [
          { id: 1, title: 'Enter Job Title', company: 'Enter Company Name', description: 'Please enter the job description...' }
        ];
      }
    } catch (err) {
      console.error('Failed to load job postings:', err);
      // Fallback data
      jobPostings = [
        { id: 1, title: 'Enter Job Title', company: 'Enter Company Name', description: 'Please enter the job description...' }
      ];
    }
  }

  async function handleGenerateCoverLetter() {
    // Check if we have the required data
    if (!selectedResume) {
      error = 'Please select a resume first';
      return;
    }

    let jobData = null;
    
    if (jobInputMethod === 'select') {
      if (!selectedJob) {
        error = 'Please select a job posting';
        return;
      }
      jobData = selectedJob;
    } else {
      // Manual input validation
      if (!manualJobTitle.trim() || !manualJobCompany.trim() || !manualJobDescription.trim()) {
        error = 'Please fill in all job details (title, company, and description)';
        return;
      }
      jobData = {
        title: manualJobTitle,
        company: manualJobCompany,
        description: manualJobDescription
      };
    }

    loading = true;
    error = null;
    success = null;

    try {
      let response;
      
      if (showCustomization) {
        // Generate customized cover letter
        const customization: CoverLetterCustomization = {
          tone: formData.tone,
          focus_areas: formData.focusAreas,
          custom_instructions: formData.customInstructions,
          include_salary_expectations: formData.includeSalary,
          include_availability: formData.includeAvailability,
          include_portfolio_link: formData.includePortfolio
        };

        response = await generateCustomizedCoverLetter(
          selectedResume.parsed_content,
          jobData.description,
          formData.companyName || jobData.company,
          formData.jobTitle || jobData.title,
          `${$user?.first_name || ''} ${$user?.last_name || ''}`,
          customization
        );
      } else {
        // Generate standard cover letter
        response = await generateCoverLetter({
          resume_id: selectedResume.id,
          job_posting_id: jobData.id || 0, // Use 0 for manual jobs
          personal_message: formData.personalMessage
        });
      }

      coverLetterContent = response.content;
      success = 'Cover letter generated successfully!';
      
      // Save to local storage
      saveCoverLetterToLocalStorage(coverLetterContent, {
        resume: selectedResume.title,
        job: jobData.title,
        company: formData.companyName || jobData.company,
        generated_at: new Date().toISOString()
      });
      
      // Refresh saved letters
      savedLetters = getSavedCoverLetters();
      
    } catch (err: any) {
      error = err.message || 'Failed to generate cover letter';
    } finally {
      loading = false;
    }
  }

  function handleTemplateSelect(template: CoverLetterTemplate) {
    selectedTemplate = template;
    // You could implement template filling logic here
  }

  function handleSaveLetter() {
    if (coverLetterContent.trim()) {
      saveCoverLetterToLocalStorage(coverLetterContent, {
        resume: selectedResume?.title || 'Unknown',
        job: selectedJob?.title || 'Unknown',
        company: formData.companyName || selectedJob?.company || 'Unknown',
        generated_at: new Date().toISOString()
      });
      savedLetters = getSavedCoverLetters();
      success = 'Cover letter saved successfully!';
    }
  }

  function handleDeleteLetter(id: number) {
    deleteSavedCoverLetter(id);
    savedLetters = getSavedCoverLetters();
    success = 'Cover letter deleted successfully!';
  }

  function copyToClipboard() {
    navigator.clipboard.writeText(coverLetterContent);
    success = 'Cover letter copied to clipboard!';
  }

  function downloadAsText() {
    const blob = new Blob([coverLetterContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cover-letter-${formData.companyName || selectedJob?.company || 'company'}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function toggleFocusArea(area: string) {
    if (formData.focusAreas.includes(area)) {
      formData.focusAreas = formData.focusAreas.filter(a => a !== area);
    } else {
      formData.focusAreas = [...formData.focusAreas, area];
    }
  }
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-2">AI Cover Letter Generator</h1>
    <p class="text-gray-600">Create personalized, professional cover letters using AI that match your </p>
    
    <!-- Model Status Indicator -->
    <div class="mt-4 flex items-center space-x-3">
      <div class="flex items-center space-x-2">
        {#if ollamaStatus === 'checking'}
          <div class="w-3 h-3 bg-yellow-500 rounded-full animate-pulse"></div>
          <span class="text-sm font-medium text-gray-700">Checking Ollama Status...</span>
        {:else if ollamaStatus === 'available'}
          <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-sm font-medium text-gray-700">Using Ollama (Llama2)</span>
        {:else}
          <div class="w-3 h-3 bg-red-500 rounded-full"></div>
          <span class="text-sm font-medium text-gray-700">Ollama Unavailable</span>
        {/if}
      </div>
      <div class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
        {ollamaStatus === 'available' ? 'Local AI Model' : 'Status: ' + ollamaStatus}
      </div>
    </div>
  </div>

  <!-- Success/Error Messages -->
  {#if success}
    <div class="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
      {success}
    </div>
  {/if}

  {#if error}
    <div class="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      {error}
    </div>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Left Column - Form -->
    <div class="lg:col-span-1 space-y-6">
      <!-- Model Information -->
      <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow p-6 border border-blue-200">
        <h3 class="text-lg font-semibold text-blue-900 mb-3">🤖 AI Model Status</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-blue-800">Model:</span>
            <span class="text-sm text-blue-600 font-semibold">Ollama (Llama2)</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-blue-800">Type:</span>
            <span class="text-sm text-blue-600">Local LLM</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-blue-800">Status:</span>
            <div class="flex items-center space-x-2">
              {#if ollamaStatus === 'checking'}
                <div class="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                <span class="text-sm text-yellow-600 font-medium">Checking...</span>
              {:else if ollamaStatus === 'available'}
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-sm text-green-600 font-medium">Active</span>
              {:else}
                <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                <span class="text-sm text-red-600 font-medium">Unavailable</span>
              {/if}
            </div>
          </div>
          <div class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded text-center">
            🚀 Powered by your local Ollama instance
          </div>
        </div>
      </div>

      <!-- Resume Selection -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Select Resume</h3>
          <button 
            on:click={loadResumes}
            class="text-sm text-primary-600 hover:text-primary-700 font-medium"
            title="Refresh resumes"
          >
            🔄 Refresh
          </button>
        </div>
        <select 
          bind:value={selectedResume}
          class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          <option value={null}>Choose a resume...</option>
          {#each resumes as resume}
            <option value={resume}>{resume.title}</option>
          {/each}
        </select>
        {#if resumes.length === 0}
          <p class="text-sm text-gray-500 mt-2">No resumes found. Please upload a resume first.</p>
        {/if}
      </div>

      <!-- Job Selection -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Job Information</h3>
          {#if jobInputMethod === 'select'}
            <button 
              on:click={loadJobPostings}
              class="text-sm text-primary-600 hover:text-primary-700 font-medium"
              title="Refresh job postings"
            >
              🔄 Refresh
            </button>
          {/if}
        </div>
        
        <!-- Job Selection or Manual Input Toggle -->
        <div class="mb-4">
          <div class="flex space-x-4">
            <label class="flex items-center">
              <input 
                type="radio" 
                bind:group={jobInputMethod} 
                value="select" 
                class="mr-2"
              />
              <span class="text-sm text-gray-700">Select from saved jobs</span>
            </label>
            <label class="flex items-center">
              <input 
                type="radio" 
                bind:group={jobInputMethod} 
                value="manual" 
                class="mr-2"
              />
              <span class="text-sm text-gray-700">Enter manually</span>
            </label>
          </div>
        </div>

        {#if jobInputMethod === 'select'}
          <select 
            bind:value={selectedJob}
            class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value={null}>Choose a job posting...</option>
            {#each jobPostings as job}
              <option value={job}>{job.title} at {job.company}</option>
            {/each}
          </select>
        {:else}
          <div class="space-y-3">
            <input 
              type="text" 
              bind:value={manualJobTitle}
              placeholder="Enter job title"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
            <input 
              type="text" 
              bind:value={manualJobCompany}
              placeholder="Enter company name"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
            <textarea 
              bind:value={manualJobDescription}
              placeholder="Enter job description..."
              rows="4"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            ></textarea>
          </div>
        {/if}
      </div>

      <!-- Basic Information -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Job Details</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
            <input 
              type="text" 
              bind:value={formData.companyName}
              placeholder="Enter company name"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
            <input 
              type="text" 
              bind:value={formData.jobTitle}
              placeholder="Enter job title"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Personal Message (Optional)</label>
            <textarea 
              bind:value={formData.personalMessage}
              placeholder="Any specific points you'd like to emphasize..."
              rows="3"
              class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Customization Toggle -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Advanced Customization</h3>
          <button 
            on:click={() => showCustomization = !showCustomization}
            class="text-primary-600 hover:text-primary-700 text-sm font-medium"
          >
            {showCustomization ? 'Hide' : 'Show'}
          </button>
        </div>
        
        {#if showCustomization}
          <div class="mt-4 space-y-4">
            <!-- Tone Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Writing Tone</label>
              <select 
                bind:value={formData.tone}
                class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                {#each toneOptions as option}
                  <option value={option.value}>{option.label} - {option.description}</option>
                {/each}
              </select>
            </div>

            <!-- Focus Areas -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Focus Areas</label>
              <div class="grid grid-cols-2 gap-2">
                {#each focusAreaOptions as area}
                  <label class="flex items-center">
                    <input 
                      type="checkbox" 
                      checked={formData.focusAreas.includes(area)}
                      on:change={() => toggleFocusArea(area)}
                      class="mr-2"
                    />
                    <span class="text-sm text-gray-700">{area}</span>
                  </label>
                {/each}
              </div>
            </div>

            <!-- Custom Instructions -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Custom Instructions</label>
              <textarea 
                bind:value={formData.customInstructions}
                placeholder="Any specific requirements or preferences..."
                rows="3"
                class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              ></textarea>
            </div>

            <!-- Additional Options -->
            <div class="space-y-2">
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  bind:checked={formData.includeSalary}
                  class="mr-2"
                />
                <span class="text-sm text-gray-700">Include salary expectations</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  bind:checked={formData.includeAvailability}
                  class="mr-2"
                />
                <span class="text-sm text-gray-700">Include availability information</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  bind:checked={formData.includePortfolio}
                  class="mr-2"
                />
                <span class="text-sm text-gray-700">Include portfolio/work samples link</span>
              </label>
            </div>

            <!-- Ollama-Specific Options -->
            <div class="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
              <h4 class="text-sm font-medium text-blue-800 mb-2">🤖 Ollama Model Settings</h4>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-blue-700">Model: Llama2 (7B)</span>
                  <span class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">Local</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-xs text-blue-700">Response Quality:</span>
                  <span class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">High</span>
                </div>
                <div class="text-xs text-blue-600 text-center">
                  ⚡ Fast local generation • 🔒 Privacy-focused • 💰 No API costs
                </div>
              </div>
            </div>
          </div>
        {/if}
      </div>

      <!-- Generate Button -->
      <button 
        on:click={handleGenerateCoverLetter}
        disabled={loading || !selectedResume || !selectedJob}
        class="w-full btn btn-primary py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if loading}
          <div class="flex items-center justify-center">
            <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            <span>Generating with Ollama...</span>
          </div>
        {:else}
          <div class="flex items-center justify-center space-x-2">
            <span>🤖 Generate with Ollama</span>
            <span class="text-sm opacity-75">(Local AI)</span>
          </div>
        {/if}
      </button>
      
      <!-- Ollama Info -->
      <div class="text-center">
        <p class="text-xs text-gray-500">
          Powered by your local Ollama instance • No external API calls • Privacy guaranteed
        </p>
      </div>
    </div>

    <!-- Right Column - Cover Letter Display -->
    <div class="lg:col-span-2 space-y-6">
      <!-- Generated Cover Letter -->
      {#if coverLetterContent}
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Generated Cover Letter</h3>
            <div class="flex space-x-2">
              <button 
                on:click={copyToClipboard}
                class="btn btn-outline text-sm"
              >
                Copy to Clipboard
              </button>
              <button 
                on:click={downloadAsText}
                class="btn btn-outline text-sm"
              >
                Download
              </button>
              <button 
                on:click={handleSaveLetter}
                class="btn btn-primary text-sm"
              >
                Save
              </button>
            </div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
            <pre class="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed">{coverLetterContent}</pre>
          </div>
        </div>
      {/if}

      <!-- Templates -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Cover Letter Templates</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          {#each templates as template}
            <div 
              class="border rounded-lg p-4 cursor-pointer hover:border-primary-300 transition-colors {selectedTemplate?.id === template.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200'}"
              on:click={() => handleTemplateSelect(template)}
            >
              <h4 class="font-medium text-gray-900 mb-2">{template.name}</h4>
              <p class="text-sm text-gray-600">{template.description}</p>
            </div>
          {/each}
        </div>
      </div>

      <!-- Saved Cover Letters -->
      {#if savedLetters.length > 0}
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Saved Cover Letters</h3>
          <div class="space-y-3">
            {#each savedLetters as letter}
              <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p class="font-medium text-gray-900">{letter.metadata.job} at {letter.metadata.company}</p>
                  <p class="text-sm text-gray-600">Generated: {new Date(letter.created_at).toLocaleDateString()}</p>
                </div>
                <div class="flex space-x-2">
                  <button 
                    on:click={() => coverLetterContent = letter.content}
                    class="btn btn-outline text-sm"
                  >
                    Load
                  </button>
                  <button 
                    on:click={() => handleDeleteLetter(letter.id)}
                    class="btn btn-outline text-sm text-red-600 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
