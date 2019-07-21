const DbxUserFiles = {
  props: {
    filesUrl: {
      type: String,
      required: true
    },
    sharedLinkUrl: {
      type: String,
      default: ''
    },
  },
  data() {
    return {
      files: '',
      processing: false
    }
  },
  methods: {
    getFiles() {
      this.files = []
      this.processing = true
      
      axios.get(this.filesUrl)
      .then(response => {
        this.files = response.data.files
        console.log(this.files)
      })
      .catch(error => {
        if (error.response) {
          console.log(error.response)
        } else if (error.request) {
          console.log(error.request)
        } else {
          console.log(error.message)
        }
        console.log(error.config)
      })
      .finally(() => {
        this.processing = false
      })
    },
    getSharedLink(path) {
      this.processing = true

      axios.post(
        this.sharedLinkUrl,
        {'dbx_path': path}
      )
      .then(response => {
        console.log(response.data)
        this.$refs['audio-url'].value = response.data['shared_link']
      })
      .catch(error => {
        if (error.response) {
          console.log(error.response)
        } else if (error.request) {
          console.log(error.request)
        } else {
          console.log(error.message)
        }
        console.log(error.config)
      })
      .finally(() => {
        this.processing = false
      })
    }
  },
  template: `
    <div>

    <input class="input" ref="audio-url" name="audio-url">

    <button
    class="button is-primary"
    v-bind:class="[{ 'is-loading': processing }]"
    @click.prevent="getFiles"
    >
    Get User dbx files
    </button>

    <div class="menu">

    <ul class="menu-list">

    <li v-for="(item, index) in files">
    <a
    @click.prevent="getSharedLink(item.path_lower)"
    > 
    {{ item.name }} 
    </a>
    </li>

    </ul>

    </div>

    </div>
  `
}

const DbxAudioFileUploader = {
  mixins: [AudioFileUploader],
  data() {
    return {
      sharedLink: ''
    }
  },
  methods: {
    success(response) {
      console.log(response)
      this.sharedLink = response.data['shared_link']
    }
  },
  template: `
    <div>
    
    <div class="file has-name is-fullwidth">

    <label class="file-label">

    <input 
    class="file-input" 
    type="file" 
    ref="file" 
    name="resume"
    @change="handleFileUpload"
    :disabled="processing"
    >

    <span class="file-cta">

    <span class="file-icon">
    <i class="fas fa-upload"></i>
    </span>

    <span class="file-label">
    <slot name="label-select-file">
    Choose a file
    </slot>
    </span>

    </span>

    <span class="file-name" ref="filename">
    </span>

    </label>

    <button 
    class="button is-primary"
    v-bind:class="[{ 'is-loading': processing }]"
    @click.prevent="submitFile"
    :disabled="file == ''"
    >

    <slot name="label-submit">
    Submit
    </slot>
    
    </button>

    </div>

    <div style="font-size: 20px;">
    {{ sharedLink }}
    </div>

    </div>
  `
}