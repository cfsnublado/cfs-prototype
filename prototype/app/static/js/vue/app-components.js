
const AlertMessage = {
  mixins: [BaseMessage],
  template: `
    <transition name="fade-transition-slow" v-on:after-enter="isOpen = true" v-on:after-leave="isOpen = false">

    <div v-show="isOpen" :class="['alert-' + messageType, 'notification']">

    <button 
    class="delete" 
    @click.prevent="close"
    >
    </button>

    {{ messageText }}

    </div>

    </transition>
  `
}

const NavbarDropdown = {
  mixins: [BaseDropdown],
  template: `
    <div 
    v-bind:id="id" 
    class="navbar-item has-dropdown" 
    v-bind:class="[{ 'is-active': isOpen }, { 'has-dropup': dropup }, dropdownClasses]"
    >

    <a class="navbar-link" @click.prevent="toggle">

    <slot name="dropdown-label">
    Dropdown
    </slot>

    </a>

    <div class="navbar-dropdown is-right">

    <slot name="dropdown-content">
      Put something here, ideally a list of menu items.
    </slot>

    </div>   

    </div>
  `  
}

const FileUploader = {
  mixins: [BaseFileUploader]
}

const AudioFileUploader = {
  mixins: [BaseFileUploader],
  methods: {
    validateFile() {
      validated = false

      if (this.file.type == 'audio/mpeg') {
        validated = true
      } else {
        console.error('Invalid file type')
      }
      
      return validated
    }
  }
}

const AudioPlayer = {
  props: {
    initAudioId: {
      type: String,
      required: true
    },
    initSoundFile: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      audioId: this.initAudioId,
      soundFile: this.initSoundFile,
      audio: null,
      playing: false,
      loaded: false
    }
  },
  watch: {
    playing(value) {
      if(value) {
        return this.audio.play()
      } else {
        return this.audio.pause()
      }
    }
  },
  mounted() {
    this.audio = this.$el.querySelector('#' + this.audioId)
    this.audio.addEventListener('loadeddata', this.loaded)
    this.audio.addEventListener('play', () => { this.playing = true })
    this.audio.addEventListener('ended', () => { this.playing = false })
  },
  template: `
    <span>
      <a @click.prevent="playing = !playing" href="#"> <i class="fas fa-volume-up"></i> </a>
      <audio :id="audioId" ref="audiofile" :src="soundFile" preload="auto" style="display: none;"></audio>
    </span>
  `
}

