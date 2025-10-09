<template>
  <div class="user-info-management">
    <h2 class="page-title">用户信息管理</h2>
    
    <!-- 添加收货地址表单 -->
    <div class="address-form" v-if="showForm">
      <h3>{{ editingAddress ? '编辑收货地址' : '添加新的收货地址' }}</h3>
      <div class="form-group">
        <label>姓名 <span class="required">*</span></label>
        <input 
          v-model="formData.name" 
          type="text" 
          placeholder="请输入姓名"
          required
        >
      </div>
      <div class="form-group">
        <label>手机号码 <span class="required">*</span></label>
        <input 
          v-model="formData.phone" 
          type="tel" 
          placeholder="请输入手机号码"
          pattern="^1[3-9]\d{9}$"
          required
        >
        <div class="error-message" v-if="phoneError">{{ phoneError }}</div>
      </div>
      <div class="form-group">
        <label>收货地址 <span class="required">*</span></label>
        <textarea 
          v-model="formData.address" 
          placeholder="请输入详细收货地址"
          rows="3"
          required
        ></textarea>
      </div>
      <div class="form-group">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="formData.is_default"
          >
          设置为默认收货地址
        </label>
      </div>
      <div class="form-actions">
        <button @click="saveAddress" class="btn-primary" :disabled="!isFormValid">
          {{ editingAddress ? '更新' : '添加' }}
        </button>
        <button @click="cancelForm" class="btn-secondary">取消</button>
      </div>
    </div>
    
    <!-- 地址列表 -->
    <div v-else>
      <button @click="showAddForm" class="btn-primary add-btn">添加新收货地址</button>
      
      <div class="address-list" v-if="addresses.length > 0">
        <div class="address-item" v-for="address in addresses" :key="address.id">
          <div class="address-header">
            <span class="address-name">{{ address.name }}</span>
            <span class="address-phone">{{ address.phone }}</span>
            <span v-if="address.is_default" class="default-tag">默认</span>
          </div>
          <div class="address-content">
            {{ address.address }}
          </div>
          <div class="address-actions">
            <button 
              @click="editAddress(address)" 
              class="btn-secondary"
              :disabled="addresses.length === 1"
            >
              编辑
            </button>
            <button 
              @click="deleteAddress(address.id)" 
              class="btn-danger"
              :disabled="addresses.length === 1"
            >
              删除
            </button>
            <button 
              @click="makeDefault(address.id)" 
              class="btn-secondary"
              :disabled="address.is_default"
            >
              设置默认
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <p>暂无收货地址，请添加</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
import { getUserAddresses, addUserAddress, updateUserAddress, deleteUserAddress, setDefaultAddress } from '@/api/userAddress';



/**
 * 用户地址信息接口
 */
export interface UserAddress {
  id: number;
  name: string;
  phone: string;
  address: string;
  is_default: boolean;
  create_time: string;
  update_time: string;
}

// 状态管理
const addresses = ref<UserAddress[]>([]);
const showForm = ref(false);
const editingAddress = ref<number | null>(null);
const phoneError = ref('');

// 表单数据
const formData = ref({
  name: '',
  phone: '',
  address: '',
  is_default: false
});

// 表单验证
const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.phone.trim() !== '' && 
         validatePhone(formData.value.phone) && 
         formData.value.address.trim() !== '';
});

// 手机号验证
function validatePhone(phone: string): boolean {
  const phoneRegex = /^1[3-9]\d{9}$/;
  const isValid = phoneRegex.test(phone);
  phoneError.value = isValid ? '' : '请输入正确的手机号码格式';
  return isValid;
}

// 加载地址列表
async function loadAddresses() {
  try {
    const data = await getUserAddresses();
    addresses.value = data;
  } catch (error) {
    ElMessage.error('获取地址列表失败');
    console.error('Failed to get addresses:', error);
  }
}

// 显示添加表单
function showAddForm() {
  resetForm();
  showForm.value = true;
  editingAddress.value = null;
}

// 编辑地址
function editAddress(address: UserAddress) {
  formData.value = {
    name: address.name,
    phone: address.phone,
    address: address.address,
    is_default: address.is_default
  };
  editingAddress.value = address.id;
  showForm.value = true;
}

// 重置表单
function resetForm() {
  formData.value = {
    name: '',
    phone: '',
    address: '',
    is_default: false
  };
  phoneError.value = '';
}

// 取消表单
function cancelForm() {
  showForm.value = false;
  editingAddress.value = null;
  resetForm();
}

// 保存地址
async function saveAddress() {
  if (!validatePhone(formData.value.phone)) {
    return;
  }
  
  try {
    if (editingAddress.value) {
      // 更新地址
      const updatedAddress = await updateUserAddress(editingAddress.value, formData.value);
      const index = addresses.value.findIndex(a => a.id === editingAddress.value);
      if (index !== -1) {
        addresses.value[index] = updatedAddress;
      }
      ElMessage.success('地址更新成功');
    } else {
      // 添加新地址
      const newAddress = await addUserAddress(formData.value);
      addresses.value.push(newAddress);
      ElMessage.success('地址添加成功');
    }
    cancelForm();
    loadAddresses(); // 重新加载地址列表以确保默认地址正确显示
  } catch (error) {
    ElMessage.error(editingAddress.value ? '地址更新失败' : '地址添加失败');
    console.error('Failed to save address:', error);
  }
}

// 删除地址
async function deleteAddress(id: number) {
  // 确认对话框
  if (!confirm('确定要删除这个收货地址吗？')) {
    return;
  }
  
  try {
    await deleteUserAddress(id);
    addresses.value = addresses.value.filter(a => a.id !== id);
    ElMessage.success('地址删除成功');
  } catch (error) {
    ElMessage.error('地址删除失败');
    console.error('Failed to delete address:', error);
  }
}

// 设置默认地址
async function makeDefault(id: number) {
  try {
    const updatedAddress = await setDefaultAddress(id);
    // 更新所有地址的默认状态
    addresses.value.forEach(a => {
      a.is_default = a.id === updatedAddress.id;
    });
    ElMessage.success('默认地址设置成功');
  } catch (error) {
    ElMessage.error('默认地址设置失败');
    console.error('Failed to set default address:', error);
  }
}





// 组件挂载时加载地址列表
onMounted(() => {
  loadAddresses();
});
</script>

<style scoped>
.user-info-management {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-title {
  margin-bottom: 20px;
  color: #333;
  font-size: 24px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.address-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-weight: 500;
}

.required {
  color: #f56c6c;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #409eff;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
  margin-right: 8px;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.add-btn {
  margin-bottom: 20px;
}

.address-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.address-item {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.address-item:hover {
  border-color: #409eff;
}

.address-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-weight: 500;
}

.address-name {
  margin-right: 15px;
}

.address-phone {
  color: #666;
}

.default-tag {
  margin-left: auto;
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.address-content {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
}

.address-actions {
  display: flex;
  gap: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

/* 按钮样式 */
.btn-primary {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #66b1ff;
}

.btn-primary:disabled {
  background-color: #c0c4cc;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #fff;
  color: #606266;
  border: 1px solid #dcdfe6;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-secondary:hover:not(:disabled) {
  color: #409eff;
  border-color: #c6e2ff;
}

.btn-secondary:disabled {
  color: #c0c4cc;
  border-color: #ebeef5;
  cursor: not-allowed;
}

.btn-danger {
  background-color: #fff;
  color: #f56c6c;
  border: 1px solid #fbc4c4;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-danger:hover:not(:disabled) {
  background-color: #fef0f0;
}

.btn-danger:disabled {
  color: #c0c4cc;
  border-color: #ebeef5;
  cursor: not-allowed;
}
</style>