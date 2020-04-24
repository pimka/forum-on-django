<template>
    <div>
        <b-form @submit="sendData">
            <h3>Create Heading</h3>
            <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
                <b-form-input id="inputHead" v-model="head" placeholder="Enter title"/>
            </b-form-group>
            <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
                <b-form-textarea id="inputBody" v-model="body" rows="5"/>
            </b-form-group>
            <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
                <b-form-select v-model="selected" :options="tags" multiple id="inputTags"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Create</b-button>
        </b-form>
    </div>
</template>

<script>
import { HTTP } from '../../api/common'

export default {
    data () {
        return {
            head: '',
            body: '',
            selected: [],
            tags: [],
        }
    },

    created () {
        this.getJSON()
    },

    methods: {
        sendData () {
            if (this.validData()) {
                HTTP.post('/headings/', {
                    'header': this.head,
                    'body': this.body,
                    'tags': this.selected
                }).then(response => {
                    this.items = response.data
                    this.err = ''
                    this.$bvToast.toast('Heaading created', {
                        title: 'Success',
                        variant: 'success'
                    })
                }).catch(err => { 
                    this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
                })
            }
        },
        validData () {
            this.createErrors = []
            if (this.selected.length == 0) {
                this.createErrors.push('Select tag')
                return false
            } else {
                return true
            }
        },
        getJSON () {
            HTTP.get('/tags/').then(response => {
                this.tags = response.data
            }).catch(err => { 
                this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
            })
        }
    }
}
</script>