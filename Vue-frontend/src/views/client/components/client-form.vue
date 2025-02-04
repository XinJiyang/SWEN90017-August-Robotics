<template>
  <el-container>
    <el-header>
      <h2>
        {{ $route.name === 'create' ? 'Add New Client' : 'Client Detail' }}
      </h2></el-header
    >
    <el-main v-loading="loading">
      <el-scrollbar>
        <el-card>
          <el-form
            ref="clientFormRef"
            :model="clientForm"
            :rules="clientFormRules"
            :hide-required-asterisk="mode === 'view' ? true : false"
            label-position="left"
            label-width="200px"
            size="large"
            status-icon
          >
            <el-form-item style="float: right">
              <el-button
                :disabled="loginStore.$state.userInfo.role === 'viewer'"
                type="danger"
                round
                @click="submitClientForm(clientFormRef)"
                >{{ $route.name === 'detail' ? 'Edit Client' : 'Save Client' }}</el-button
              >
            </el-form-item>
            <el-form-item label="Name" prop="venue_name">
              <el-input
                v-model="clientForm.venue_name"
                :readonly="mode === 'view' ? true : false"
              />
            </el-form-item>
            <el-form-item label="Region" prop="region">
              <el-select v-model="clientForm.region" :disabled="mode === 'view' ? true : false">
                <el-option v-for="item in countries" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
            <el-form-item label="Email" prop="email">
              <el-input
                v-model="clientForm.email"
                placeholder="Ex: user1@gmail.com"
                :readonly="mode === 'view' ? true : false"
              />
            </el-form-item>
            <el-form-item label="Phone Number" prop="phone">
              <el-input
                v-model="clientForm.phone"
                placeholder="Ex: 0392389889"
                :readonly="mode === 'view' ? true : false"
              />
            </el-form-item>
            <el-form-item style="float: right">
              <el-button
                type="success"
                round
                @click="dialogFormVisible = true"
                :disabled="mode === 'view' ? true : false"
                >Add Halls</el-button
              >
            </el-form-item>
            <el-form-item label="Venue Information"> </el-form-item>
          </el-form>
          <el-table :data="clientForm.halls" :max-height="tableHeight">
            <el-table-column prop="hall" label="Halls" />
            <el-table-column prop="area" label="Gross Area(Sqm)" />
          </el-table>
        </el-card>
      </el-scrollbar>
    </el-main>
    <el-dialog
      v-model="dialogFormVisible"
      center
      align-center
      style="border-radius: 20px"
      width="400px"
      @close="resetVenueForm(venueFormRef)"
    >
      <el-form
        ref="venueFormRef"
        :model="venueForm"
        :rules="venueFormRules"
        label-position="left"
        label-width="180px"
        size="large"
      >
        <el-form-item label="Hall" prop="hall">
          <el-input v-model="venueForm.hall" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Gross Area(Sqm)" prop="area">
          <el-input-number
            v-model="venueForm.area"
            :step="100"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button round type="danger" size="large" @click="resetVenueForm(venueFormRef)"
          >Cancel</el-button
        >
        <el-button round type="success" size="large" @click="submitVenueForm(venueFormRef)"
          >Save</el-button
        >
      </template>
    </el-dialog>
  </el-container>
  <!-- <div>
    <div class="text-h6" style="padding: 30px 0px 0px 30px">{{ $route.name === "create" ? "Add New Client" : "Client Detail"}}</div>
    <v-card class="h-auto" style="padding: 20px; margin: 30px">
      <v-form ref="clientForm" validate-on="blur" :readonly="mode === 'view' ? true : false">
        <v-container>
          <v-row>
            <v-col cols="2">
              <label>Venue Name</label>
            </v-col>
            <v-col cols="4" lg="3">
              <v-text-field
                :density="lgAndUp ? 'default' : 'compact'"
                style="margin-top: 10px"
                variant="solo-filled"
                v-model="client.venue_name"
                placeholder="Name"
                :rules="[() => !!client.venue_name || 'This field is required']"
                required
              ></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col cols="2" xl="1">
              <v-btn @click="validateClient" rounded="lg" color="red" max-width="150"
                >{{ $route.name === "detail" ? "Edit Client" : "Save Client"}}
                <v-dialog v-model="confirmSave" width="auto">
                  <v-card>
                    <v-card-text> Are you sure you want to create a new Client? </v-card-text>
                    <v-card-actions>
                      <v-btn @click="saveClient">Save</v-btn>
                      <v-spacer></v-spacer>
                      <v-btn color="red" @click="confirmSave = false">Cancel</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2">
              <label>Region</label>
            </v-col>
            <v-col cols="4" lg="3">
              <v-autocomplete
                :density="lgAndUp ? 'default' : 'compact'"
                variant="solo-filled"
                v-model="client.region"
                :rules="[() => !!client.region || 'This field is required']"
                :items=countries
                placeholder="Select Region"
                required
              ></v-autocomplete>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2">
              <label>Email</label>
            </v-col>
            <v-col cols="4" lg="3">
              <v-text-field
                :density="lgAndUp ? 'default' : 'compact'"
                variant="solo-filled"
                v-model="client.email"
                :rules="[
                  () => !!client.email || 'This field is required',
                  () =>
                    (!!client.email &&
                      client.email.match(
                        /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/
                      ) != null) ||
                    'Incorrect email format. Ex: user1@gmail.com'
                ]"
                placeholder="Ex: user1@gmail.com"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2">
              <label>Phone Number</label>
            </v-col>
            <v-col cols="4" lg="3">
              <v-text-field
                :density="lgAndUp ? 'default' : 'compact'"
                variant="solo-filled"
                v-model="client.phone"
                placeholder="Ex: 0392389889"
                :rules="[
                  () => !!client.phone || 'This field is required',
                  () =>
                    (!!client.phone && client.phone.match(/^[0-9]+$/) != null) ||
                    'Incorrect phone number format. Ex: 0392389889'
                ]"
              ></v-text-field>
            </v-col>
          </v-row>
          <ClientVenue :venues="client.halls" :mode="mode"/>
        </v-container>
      </v-form>
    </v-card>
  </div> -->
</template>

<script setup lang="ts">
import useClientStore from '@/stores/client/client';
import { useRouter, useRoute } from 'vue-router';
import type { IClient, IVenue } from '@/types';
import { ref, onMounted, onBeforeUnmount, reactive } from 'vue';
import { countries } from '@/utils/country';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import useLoginStore from '@/stores/login/login';

// routes
const router = useRouter();
const route = useRoute();

// store
const clientStore = useClientStore();
const loginStore = useLoginStore();

// emits & props
const emit = defineEmits(['createClient', 'updateClient']);
defineProps<{ mode: string }>();

// venue Dialog
const dialogFormVisible = ref(false);
const venueFormRef = ref<FormInstance>();
const venueForm = reactive<IVenue>({
  hall: '',
  area: 0
});
const venueFormRules = reactive<FormRules>({
  hall: [{ required: true, message: 'Please input hall name', trigger: 'blur' }],
  area: [
    { type: 'number', required: true, message: 'Please input gross area', trigger: 'change' },
    { type: 'number', min: 0, message: 'Area cannot be negative', trigger: 'blur' }
  ]
});

async function submitVenueForm(form: FormInstance | undefined) {
  if (!form) return;
  await form.validate((valid, fields) => {
    if (valid) {
      clientForm.halls.push({ ...venueForm });
      dialogFormVisible.value = false;
    }
  });
}

function resetVenueForm(form: FormInstance | undefined) {
  if (!form) return;
  form.resetFields();
  dialogFormVisible.value = false;
}

// Venue Table
const tableHeight = ref(0);

function updateMaxHeight() {
  tableHeight.value = Math.max(window.innerHeight - 600, 120);
}

// client form
const loading = ref(false);
const clientFormRef = ref<FormInstance>();
const clientForm = reactive<IClient>({
  id: '',
  venue_name: '',
  region: undefined,
  email: '',
  phone: '',
  halls: []
});
const clientFormRules = reactive<FormRules>({
  venue_name: [{ required: true, message: 'Please input name', trigger: 'blur' }],
  region: [{ required: true, message: 'Please select region', trigger: 'blur' }],
  email: [
    { required: true, message: 'Please input email', trigger: 'blur' },
    { type: 'email', message: 'Please input valid email', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: 'Please input phone number', trigger: 'blur' },
    { pattern: /^\+?(\d[\d-. ]+)?(\([\d-. ]+\))?[\d-. ]+\d$/, message: 'Please input valid phone number', trigger: 'blur' }
  ]
});

async function submitClientForm(form: FormInstance | undefined) {
  if (route.name === 'detail') {
    // change to edit mode
    router.push('/client/edit/' + route.params.id);
  } else {
    // TODO: check if any change has been made

    // check whether form value pass validation
    if (!form) return;
    await form.validate((valid, fields) => {
      if (valid) {
        if (route.name === 'create') {
          emit('createClient', clientForm);
        }
        if (route.name === 'edit') {
          emit('updateClient', clientForm);
        }
      }
    });
  }
}

// component lifecycle
onMounted(async () => {
  // Only need to load client info if it exist
  if (route.params.id !== undefined) {
    // extract client id from route params
    let id: string;
    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }

    // find client based on id
    loading.value = true;
    let clientInfo = await clientStore.getClient(id);
    if (clientInfo === undefined) {
      // cannot find client
      ElMessage.error('Cannot find requested client');
    } else {
      // set retrieved value as default value
      clientForm.id = clientInfo.id;
      clientForm.venue_name = clientInfo.venue_name;
      clientForm.email = clientInfo.email;
      clientForm.phone = clientInfo.phone;
      clientForm.region = clientInfo.region;
      clientForm.halls = clientInfo.halls;
    }
    loading.value = false;
  }

  // update max height for table
  updateMaxHeight();

  // make table responsive when window resize
  window.addEventListener('resize', updateMaxHeight);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateMaxHeight);
});
</script>

<style lang="less" scoped>
* {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: bold;
  color: gray;
  --el-color-primary: green;
}

.el-container {
  padding: 30px;
  background-color: #f6f6f6;
  border-radius: 20px;
  height: 100%;
}

.el-main,
.el-header {
  padding: 0px;
}

.el-card {
  padding: 5px 30px;
  height: 100%;
}

.el-button {
  color: white;
}

.el-table {
  width: 100%;
  border-top: 1px solid LightGrey;
}

.el-select,
.el-input,
.el-input-number {
  width: 200px;
}
</style>
