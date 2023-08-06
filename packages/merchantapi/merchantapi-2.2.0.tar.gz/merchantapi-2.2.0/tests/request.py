"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import time
import random
from . import helper
import merchantapi.request
import merchantapi.response
import merchantapi.model
import merchantapi.multicall
from . credentials import MerchantApiTestCredentials
import datetime
import json

helper.configure_logging()
helper.configure_permissions()


def test_availability_group_business_account_update_assigned():
	"""
	Tests the AvailabilityGroupBusinessAccount_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupBusinessAccount_Update_Assigned.xml')

	availability_group_business_account_update_assigned_test_assignment()
	availability_group_business_account_update_assigned_test_unassignment()
	availability_group_business_account_update_assigned_test_invalid_assign()
	availability_group_business_account_update_assigned_test_invalid_availability_group()
	availability_group_business_account_update_assigned_test_invalid_business_account()


def availability_group_business_account_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_business_account():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('InvalidBusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def test_availability_group_customer_update_assigned():
	"""
	Tests the AvailabilityGroupCustomer_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupCustomer_Update_Assigned.xml')

	availability_group_customer_update_assigned_test_assignment()
	availability_group_customer_update_assigned_test_unassignment()
	availability_group_customer_update_assigned_test_invalid_assign()
	availability_group_customer_update_assigned_test_invalid_availability_group()
	availability_group_customer_update_assigned_test_invalid_customer()


def availability_group_customer_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupCustomerUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCustUpdateAssigned')\
		.set_customer_login('AvailabilityGrpCustUpdateAssigned')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCustomerUpdateAssigned)


def availability_group_customer_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupCustomerUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCustUpdateAssigned')\
		.set_customer_login('AvailabilityGrpCustUpdateAssigned')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCustomerUpdateAssigned)


def availability_group_customer_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupCustomerUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpCustUpdateAssigned')\
		.set_customer_login('AvailabilityGrpCustUpdateAssigned')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupCustomerUpdateAssigned)


def availability_group_customer_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupCustomerUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_customer_login('AvailabilityGrpCustUpdateAssigned')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupCustomerUpdateAssigned)


def availability_group_customer_update_assigned_test_invalid_customer():
	request = merchantapi.request.AvailabilityGroupCustomerUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCustUpdateAssigned')\
		.set_customer_login('InvalidAvailabilityGroupCustomer')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupCustomerUpdateAssigned)


def test_availability_group_list_load_query():
	"""
	Tests the AvailabilityGroupList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupList_Load_Query.xml')

	availability_group_list_load_query_test_list_load()


def availability_group_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('name', 'AvailabilityGroupListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupListLoadQuery)

	assert isinstance(response.get_availability_groups(), list)

	for i, ag in enumerate(response.get_availability_groups()):
		assert isinstance(ag, merchantapi.model.AvailabilityGroup)
		assert ag.get_name() == ('AvailabilityGroupListLoadQueryTest_%d' % int(i+1))


def test_availability_group_payment_method_update_assigned():
	"""
	Tests the AvailabilityGroupPaymentMethod_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupPaymentMethod_Update_Assigned.xml')

	availability_group_payment_method_update_assigned_test_assignment()
	availability_group_payment_method_update_assigned_test_unassignment()
	availability_group_payment_method_update_assigned_test_invalid_assign()
	availability_group_payment_method_update_assigned_test_invalid_availability_group()


def availability_group_payment_method_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupPaymentMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpPayMethUpdateAssignedTest')\
		.set_module_code('COD')\
		.set_method_code('COD')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned)


def availability_group_payment_method_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupPaymentMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpPayMethUpdateAssignedTest')\
		.set_module_code('COD')\
		.set_method_code('COD')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned)


def availability_group_payment_method_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupPaymentMethodUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpPayMethUpdateAssignedTest')\
		.set_module_code('COD')\
		.set_method_code('COD')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned)


def availability_group_payment_method_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupPaymentMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_module_code('COD')\
		.set_method_code('COD')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupPaymentMethodUpdateAssigned)


def test_availability_group_product_update_assigned():
	"""
	Tests the AvailabilityGroupProduct_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupProduct_Update_Assigned.xml')

	availability_group_product_update_assigned_test_assignment()
	availability_group_product_update_assigned_test_unassignment()
	availability_group_product_update_assigned_test_invalid_assign()
	availability_group_product_update_assigned_test_invalid_availability_group()
	availability_group_product_update_assigned_test_invalid_product()


def availability_group_product_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_product():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('InvalidProduct')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def test_availability_group_shipping_method_update_assigned():
	"""
	Tests the AvailabilityGroupShippingMethod_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupShippingMethod_Update_Assigned.xml')

	availability_group_shipping_method_update_assigned_test_assignment()
	availability_group_shipping_method_update_assigned_test_unassignment()
	availability_group_shipping_method_update_assigned_test_invalid_assign()
	availability_group_shipping_method_update_assigned_test_invalid_availability_group()


def availability_group_shipping_method_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def test_category_list_load_parent():
	"""
	Tests the CategoryList_Load_Parent API Call
	"""

	helper.provision_store('CategoryList_Load_Parent.xml')

	category_list_load_parent_test_list_load()


def category_list_load_parent_test_list_load():
	parentcat = helper.get_category('CategoryListLoadParentTest_Parent')

	assert parentcat is not None
	assert isinstance(parentcat, merchantapi.model.Category)

	request = merchantapi.request.CategoryListLoadParent(helper.init_client(), parentcat)

	assert request.get_parent_id() == parentcat.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadParent)

	assert len(response.get_categories()) == 3

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadParentTest_Child_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadParentTest_Child_%d' % int(i+1)
		assert category.get_active() is True


def test_category_list_load_query():
	"""
	Tests the CategoryList_Load_Query API Call
	"""

	helper.provision_store('CategoryList_Load_Query.xml')
	helper.upload_image('graphics/CategoryListLoadQuery1.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery2.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery3.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery4.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery5.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery6.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery7.jpg')

	category_list_load_query_test_list_load()
	category_list_load_query_test_list_load_with_custom_fields()


def category_list_load_query_test_list_load():
	request = merchantapi.request.CategoryListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CategoryListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadQuery)

	assert isinstance(response.get_categories(), list)
	assert len(response.get_categories()) == 7

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadQueryTest_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadQueryTest_%d' % int(i+1)


def category_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.CategoryListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CategoryListLoadQueryTest_%'))\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_checkbox')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_imageupload')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_text')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_textarea')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_dropdown')\
		.set_sort('code', merchantapi.request.CategoryListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadQuery)

	assert isinstance(response.get_categories(), list)
	assert len(response.get_categories()) == 7

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadQueryTest_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadQueryTest_%d' % int(i+1)

		assert isinstance(category.get_custom_field_values(), merchantapi.model.CustomFieldValues)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_checkbox', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_checkbox', 'customfields') == '1'

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_imageupload', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/CategoryListLoadQuery%d.jpg' % int(i+1)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_text', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_text', 'customfields') == 'CategoryListLoadQueryTest_%d' % int(i+1)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_dropdown', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i+1)


def test_category_product_update_assigned():
	"""
	Tests the CategoryProduct_Update_Assigned API Call
	"""

	helper.provision_store('CategoryProduct_Update_Assigned.xml')

	category_product_update_assigned_test_assignment()
	category_product_update_assigned_test_unassignment()
	category_product_update_assigned_test_invalid_assign()
	category_product_update_assigned_test_invalid_category()
	category_product_update_assigned_test_invalid_product()


def category_product_update_assigned_test_assignment():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_unassignment():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_category():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('InvalidCategory')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_product():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('InvalidProduct')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)


def test_category_insert():
	"""
	Tests the Category_Insert API Call
	"""

	helper.provision_store('Category_Insert.xml')

	category_insert_test_insertion()
	category_insert_test_insertion_with_custom_fields()


def category_insert_test_insertion():
	request = merchantapi.request.CategoryInsert(helper.init_client())

	request.set_category_code('CategoryInsertTest_1')\
		.set_category_name('CategoryInsertTest_1 Name')\
		.set_category_page_title('CategoryInsertTest_1 Page Title')\
		.set_category_active(True)\
		.set_category_parent_category('')\
		.set_category_alternate_display_page('')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryInsert)

	assert isinstance(response.get_category(), merchantapi.model.Category)
	assert response.get_category().get_code() == 'CategoryInsertTest_1'
	assert response.get_category().get_name() == 'CategoryInsertTest_1 Name'
	assert response.get_category().get_page_title() == 'CategoryInsertTest_1 Page Title'
	assert response.get_category().get_active() is True
	assert response.get_category().get_id() > 0

	check = helper.get_category('CategoryInsertTest_1')

	assert isinstance(check, merchantapi.model.Category)
	assert check.get_id() == response.get_category().get_id()


def category_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.CategoryInsert(helper.init_client())

	request.set_category_code('CategoryInsertTest_2')\
		.set_category_name('CategoryInsertTest_2 Name')\
		.set_category_page_title('CategoryInsertTest_2 Page Title')\
		.set_category_active(True)\
		.set_category_parent_category('')\
		.set_category_alternate_display_page('')

	request.get_custom_field_values() \
		.add_value('CategoryInsertTest_checkbox', 'True', 'customfields') \
		.add_value('CategoryInsertTest_imageupload', 'graphics/00000001/CategoryInsert.jpg', 'customfields') \
		.add_value('CategoryInsertTest_text', 'CategoryInsertTest_2', 'customfields') \
		.add_value('CategoryInsertTest_textarea', 'CategoryInsertTest_2', 'customfields') \
		.add_value('CategoryInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryInsert)
	assert isinstance(response.get_category(), merchantapi.model.Category)

	check = helper.get_category('CategoryInsertTest_2')

	assert isinstance(check, merchantapi.model.Category)
	assert check.get_code() == 'CategoryInsertTest_2'
	assert check.get_name() == 'CategoryInsertTest_2 Name'
	assert check.get_page_title() == 'CategoryInsertTest_2 Page Title'
	assert check.get_active() is True
	assert check.get_id() > 0

	assert isinstance(check.get_custom_field_values(), merchantapi.model.CustomFieldValues)

	assert check.get_custom_field_values().has_value('CategoryInsertTest_checkbox', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_checkbox', 'customfields') == '1'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_imageupload', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_imageupload', 'customfields') == 'graphics/00000001/CategoryInsert.jpg'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_text', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_text', 'customfields') == 'CategoryInsertTest_2'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_textarea', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_textarea', 'customfields') == 'CategoryInsertTest_2'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_dropdown', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_dropdown', 'customfields') == 'Option2'


def test_category_delete():
	"""
	Tests the Category_Delete API Call
	"""

	helper.provision_store('Category_Delete.xml')

	category_delete_test_deletion()
	category_delete_test_invalid_category()


def category_delete_test_deletion():
	request = merchantapi.request.CategoryDelete(helper.init_client())

	request.set_edit_category('CategoryDeleteTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryDelete)

	check = helper.get_category('CategoryDelete')
	assert check is None


def category_delete_test_invalid_category():
	request = merchantapi.request.CategoryDelete(helper.init_client())

	request.set_edit_category('InvalidCategory')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryDelete)


def test_category_update():
	"""
	Tests the Category_Update API Call
	"""

	helper.provision_store('Category_Update.xml')

	category_update_test_update()


def category_update_test_update():
	request = merchantapi.request.CategoryUpdate(helper.init_client())

	request.set_edit_category('CategoryUpdateTest_01')\
		.set_category_name('CategoryUpdateTest_01 New Name')\
		.set_category_active(False)\
		.set_category_page_title('CategoryUpdateTest_01 New Page Title')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryUpdate)

	check = helper.get_category('CategoryUpdateTest_01')

	assert check is not None
	assert check.get_code() == 'CategoryUpdateTest_01'
	assert check.get_name() == 'CategoryUpdateTest_01 New Name'
	assert check.get_page_title() == 'CategoryUpdateTest_01 New Page Title'
	assert check.get_active() is False


def test_coupon_list_delete():
	"""
	Tests the CouponList_Delete API Call
	"""

	helper.provision_store('CouponList_Delete.xml')

	coupon_list_delete_test_deletion()


def coupon_list_delete_test_deletion():
	listrequest = merchantapi.request.CouponListLoadQuery(helper.init_client())

	listrequest.set_filters(listrequest.filter_expression().like('code', 'CouponListDeleteTest_%'))

	listresponse = listrequest.send()

	helper.validate_response_success(listresponse, merchantapi.response.CouponListLoadQuery)

	assert len(listresponse.get_coupons()) == 3

	request = merchantapi.request.CouponListDelete(helper.init_client())

	for coupon in listresponse.get_coupons():
		request.add_coupon(coupon)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponListDelete)


def test_coupon_list_load_query():
	"""
	Tests the CouponList_Load_Query API Call
	"""

	helper.provision_store('CouponList_Load_Query.xml')

	coupon_list_load_query_test_list_load()


def coupon_list_load_query_test_list_load():
	request = merchantapi.request.CouponListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CouponListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponListLoadQuery)

	assert isinstance(response.get_coupons(), list)
	assert len(response.get_coupons()) == 3

	for i, coupon in enumerate(response.get_coupons()):
		assert isinstance(coupon, merchantapi.model.Coupon)
		assert coupon.get_code() == 'CouponListLoadQueryTest_%d' % int(i+1)


def test_coupon_price_group_update_assigned():
	"""
	Tests the CouponPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('CouponPriceGroup_Update_Assigned.xml')

	coupon_price_group_update_assigned_test_assignment()
	coupon_price_group_update_assigned_test_unassignment()
	coupon_price_group_update_assigned_test_invalid_assign()
	coupon_price_group_update_assigned_invalid_price_group()
	coupon_price_group_update_assigned_invalid_coupon()


def coupon_price_group_update_assigned_test_assignment():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_test_unassignment():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_test_invalid_assign():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_invalid_price_group():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('InvalidPriceGroup')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_invalid_coupon():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('InvalidCoupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def test_coupon_insert():
	"""
	Tests the Coupon_Insert API Call
	"""

	helper.provision_store('Coupon_Insert.xml')

	coupon_insert_test_insertion()
	coupon_insert_test_insertion_with_price_group()
	coupon_insert_test_duplicate_code()
	coupon_insert_test_invalid_price_group()


def coupon_insert_test_insertion():
	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_1')\
		.set_description('CouponInsertTest_1 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponInsert)
	assert isinstance(response.get_coupon(), merchantapi.model.Coupon)
	assert response.get_coupon().get_code() == 'CouponInsertTest_1'
	assert response.get_coupon().get_description() == 'CouponInsertTest_1 Description'
	assert response.get_coupon().get_customer_scope() == merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS
	assert response.get_coupon().get_date_time_start() == start_time
	assert response.get_coupon().get_date_time_end() == end_time
	assert response.get_coupon().get_max_per() == 1
	assert response.get_coupon().get_max_use() == 2
	assert response.get_coupon().get_active() is True

	coupon = helper.get_coupon('CouponInsertTest_1')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_id() == response.get_coupon().get_id()


def coupon_insert_test_insertion_with_price_group():
	price_group = helper.get_price_group('CouponInsertTest_PriceGroup')

	assert isinstance(price_group, merchantapi.model.PriceGroup)
	assert price_group.get_id() > 0

	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_2')\
		.set_description('CouponInsertTest_2 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)\
		.set_price_group_id(price_group.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponInsert)
	assert isinstance(response.get_coupon(), merchantapi.model.Coupon)
	assert response.get_coupon().get_code() == 'CouponInsertTest_2'
	assert response.get_coupon().get_description() == 'CouponInsertTest_2 Description'
	assert response.get_coupon().get_customer_scope() == merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS
	assert response.get_coupon().get_date_time_start() == start_time
	assert response.get_coupon().get_date_time_end() == end_time
	assert response.get_coupon().get_max_per() == 1
	assert response.get_coupon().get_max_use() == 2
	assert response.get_coupon().get_active() is True

	coupon = helper.get_coupon('CouponInsertTest_2')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_id() == response.get_coupon().get_id()


def coupon_insert_test_duplicate_code():
	request = merchantapi.request.CouponInsert(helper.init_client())

	request.set_code('CouponInsertTest_Duplicate')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponInsert)


def coupon_insert_test_invalid_price_group():
	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_2')\
		.set_description('CouponInsertTest_2 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)\
		.set_price_group_id(8569545)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponInsert)


def test_coupon_update():
	"""
	Tests the Coupon_Update API Call
	"""

	helper.provision_store('Coupon_Update.xml')

	coupon_update_test_update()


def coupon_update_test_update():
	request = merchantapi.request.CouponUpdate(helper.init_client())

	request.set_edit_coupon('CouponUpdateTest')\
		.set_max_use(1000)\
		.set_max_per(2)\
		.set_active(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponUpdate)

	coupon = helper.get_coupon('CouponUpdateTest')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_code() == 'CouponUpdateTest'
	assert coupon.get_max_per() == 2
	assert coupon.get_max_use() == 1000
	assert coupon.get_active() is True


def test_customer_list_load_query():
	"""
	Tests the CustomerList_Load_Query API Call
	"""

	helper.provision_store('CustomerList_Load_Query.xml')
	helper.upload_image('graphics/CustomerListLoadQuery1.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery2.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery3.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery4.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery5.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery6.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery7.jpg')

	customer_list_load_query_test_list_load()
	customer_list_load_query_test_list_load_with_custom_fields()


def customer_list_load_query_test_list_load():
	request = merchantapi.request.CustomerListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('login', 'CustomerListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerListLoadQuery)

	assert isinstance(response.get_customers(), list)
	assert len(response.get_customers()) == 7

	for i, customer in enumerate(response.get_customers()):
		assert isinstance(customer, merchantapi.model.Customer)
		assert customer.get_login() == 'CustomerListLoadQueryTest_%d' % int(i+1)


def customer_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.CustomerListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('login', 'CustomerListLoadQueryTest_%'))\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_checkbox')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_imageupload')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_text')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_textarea')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_dropdown')\
		.set_sort('login', merchantapi.request.CustomerListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerListLoadQuery)

	assert isinstance(response.get_customers(), list)
	assert len(response.get_customers()) == 7

	for i, customer in enumerate(response.get_customers()):
		assert isinstance(customer, merchantapi.model.Customer)
		assert customer.get_login() == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert isinstance(customer.get_custom_field_values(), merchantapi.model.CustomFieldValues)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_checkbox', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_checkbox', 'customfields') == '1'
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_imageupload', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/CustomerListLoadQuery%d.jpg' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_text', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_text', 'customfields') == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_textarea', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_textarea', 'customfields') == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_dropdown', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i+1)


def test_customer_delete():
	"""
	Tests the Customer_Delete API Call
	"""

	helper.provision_store('Customer_Delete.xml')

	customer_delete_test_deletion()
	customer_delete_test_invalid_customer()


def customer_delete_test_deletion():
	request = merchantapi.request.CustomerDelete(helper.init_client())

	request.set_edit_customer('CustomerDeleteTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerDelete)

	customer = helper.get_customer('CustomerDeleteTest')

	assert customer is None


def customer_delete_test_invalid_customer():
	request = merchantapi.request.CustomerDelete(helper.init_client())

	request.set_edit_customer('InvalidCustomerLogin')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CustomerDelete)


def test_customer_insert():
	"""
	Tests the Customer_Insert API Call
	"""

	helper.provision_store('Customer_Insert.xml')

	customer_insert_test_insertion()
	customer_insert_test_insertion_with_custom_fields()
	customer_insert_test_duplicate_customer()


def customer_insert_test_insertion():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_1') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \
		.set_customer_bill_first_name('John') \
		.set_customer_bill_last_name('Doe') \
		.set_customer_bill_address1('1234 Some St') \
		.set_customer_bill_address2('Unit 100') \
		.set_customer_bill_city('San Diego') \
		.set_customer_bill_state('CA') \
		.set_customer_bill_zip('92009') \
		.set_customer_bill_country('USA') \
		.set_customer_bill_company('Miva Inc') \
		.set_customer_bill_phone('6191231234') \
		.set_customer_bill_fax('6191234321') \
		.set_customer_bill_email('test@coolcommerce.net') \
		.set_customer_ship_first_name('John') \
		.set_customer_ship_last_name('Deer') \
		.set_customer_ship_address1('4321 Some St') \
		.set_customer_ship_address2('Unit 200') \
		.set_customer_ship_city('San Diego') \
		.set_customer_ship_state('CA') \
		.set_customer_ship_zip('92009') \
		.set_customer_ship_phone('6191231234') \
		.set_customer_ship_fax('6191234321') \
		.set_customer_ship_email('test@coolcommerce.net') \
		.set_customer_ship_country('USA') \
		.set_customer_ship_company('Miva Inc')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerInsert)

	assert isinstance(response.get_customer(), merchantapi.model.Customer)
	assert response.get_customer().get_password_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_bill_first_name() == 'John'
	assert response.get_customer().get_bill_last_name() == 'Doe'
	assert response.get_customer().get_bill_address1() == '1234 Some St'
	assert response.get_customer().get_bill_address2() == 'Unit 100'
	assert response.get_customer().get_bill_city() == 'San Diego'
	assert response.get_customer().get_bill_state() == 'CA'
	assert response.get_customer().get_bill_zip() == '92009'
	assert response.get_customer().get_bill_country() == 'USA'
	assert response.get_customer().get_bill_company() == 'Miva Inc'
	assert response.get_customer().get_bill_phone() == '6191231234'
	assert response.get_customer().get_bill_fax() == '6191234321'
	assert response.get_customer().get_bill_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_ship_first_name() == 'John'
	assert response.get_customer().get_ship_last_name() == 'Deer'
	assert response.get_customer().get_ship_address1() == '4321 Some St'
	assert response.get_customer().get_ship_address2() == 'Unit 200'
	assert response.get_customer().get_ship_city() == 'San Diego'
	assert response.get_customer().get_ship_state() == 'CA'
	assert response.get_customer().get_ship_zip() == '92009'
	assert response.get_customer().get_ship_phone() == '6191231234'
	assert response.get_customer().get_ship_fax() == '6191234321'
	assert response.get_customer().get_ship_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_ship_country() == 'USA'
	assert response.get_customer().get_ship_company() == 'Miva Inc'

	customer = response.get_customer()

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_id() == response.get_customer().get_id()


def customer_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_2') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \
		.set_customer_bill_first_name('John') \
		.set_customer_bill_last_name('Doe') \
		.set_customer_bill_address1('1234 Some St') \
		.set_customer_bill_address2('Unit 100') \
		.set_customer_bill_city('San Diego') \
		.set_customer_bill_state('CA') \
		.set_customer_bill_zip('92009') \
		.set_customer_bill_country('USA') \
		.set_customer_bill_company('Miva Inc') \
		.set_customer_bill_phone('6191231234') \
		.set_customer_bill_fax('6191234321') \
		.set_customer_bill_email('test@coolcommerce.net') \
		.set_customer_ship_first_name('John') \
		.set_customer_ship_last_name('Deer') \
		.set_customer_ship_address1('4321 Some St') \
		.set_customer_ship_address2('Unit 200') \
		.set_customer_ship_city('San Diego') \
		.set_customer_ship_state('CA') \
		.set_customer_ship_zip('92009') \
		.set_customer_ship_phone('6191231234') \
		.set_customer_ship_fax('6191234321') \
		.set_customer_ship_email('test@coolcommerce.net') \
		.set_customer_ship_country('USA') \
		.set_customer_ship_company('Miva Inc')

	request.get_custom_field_values()\
		.add_value('CustomerInsertTest_checkbox', 'True', 'customfields')\
		.add_value('CustomerInsertTest_imageupload', 'graphics/00000001/CustomerInsert.jpg', 'customfields')\
		.add_value('CustomerInsertTest_text', 'CustomerInsertTest_2', 'customfields')\
		.add_value('CustomerInsertTest_textarea', 'CustomerInsertTest_2', 'customfields')\
		.add_value('CustomerInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerInsert)

	customer = helper.get_customer('CustomerInsertTest_2')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_password_email() == 'test@coolcommerce.net'
	assert customer.get_bill_first_name() == 'John'
	assert customer.get_bill_last_name() == 'Doe'
	assert customer.get_bill_address1() == '1234 Some St'
	assert customer.get_bill_address2() == 'Unit 100'
	assert customer.get_bill_city() == 'San Diego'
	assert customer.get_bill_state() == 'CA'
	assert customer.get_bill_zip() == '92009'
	assert customer.get_bill_country() == 'USA'
	assert customer.get_bill_company() == 'Miva Inc'
	assert customer.get_bill_phone() == '6191231234'
	assert customer.get_bill_fax() == '6191234321'
	assert customer.get_bill_email() == 'test@coolcommerce.net'
	assert customer.get_ship_first_name() == 'John'
	assert customer.get_ship_last_name() == 'Deer'
	assert customer.get_ship_address1() == '4321 Some St'
	assert customer.get_ship_address2() == 'Unit 200'
	assert customer.get_ship_city() == 'San Diego'
	assert customer.get_ship_state() == 'CA'
	assert customer.get_ship_zip() == '92009'
	assert customer.get_ship_phone() == '6191231234'
	assert customer.get_ship_fax() == '6191234321'
	assert customer.get_ship_email() == 'test@coolcommerce.net'
	assert customer.get_ship_country() == 'USA'
	assert customer.get_ship_company() == 'Miva Inc'

	assert isinstance(customer.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_checkbox', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_checkbox', 'customfields') == '1'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_imageupload', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_imageupload', 'customfields') == 'graphics/00000001/CustomerInsert.jpg'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_text', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_text', 'customfields') == 'CustomerInsertTest_2'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_textarea', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_textarea', 'customfields') == 'CustomerInsertTest_2'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_dropdown', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_dropdown', 'customfields') == 'Option2'


def customer_insert_test_duplicate_customer():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_Duplicate') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CustomerInsert)


def test_customer_update():
	"""
	Tests the Customer_Update API Call
	"""

	helper.provision_store('Customer_Update.xml')

	customer_update_test_update()


def customer_update_test_update():
	request = merchantapi.request.CustomerUpdate(helper.init_client())

	request.set_edit_customer('CustomerUpdateTest_01') \
		.set_customer_password_email('test@coolcommerce.net') \
		.set_customer_bill_first_name('John') \
		.set_customer_bill_last_name('Doe') \
		.set_customer_bill_address1('1234 Some St') \
		.set_customer_bill_address2('Unit 100') \
		.set_customer_bill_city('San Diego') \
		.set_customer_bill_state('CA') \
		.set_customer_bill_zip('92009') \
		.set_customer_bill_country('USA') \
		.set_customer_bill_company('Miva Inc') \
		.set_customer_bill_phone('6191231234') \
		.set_customer_bill_fax('6191234321') \
		.set_customer_bill_email('test@coolcommerce.net') \
		.set_customer_ship_first_name('John') \
		.set_customer_ship_last_name('Deer') \
		.set_customer_ship_address1('4321 Some St') \
		.set_customer_ship_address2('Unit 200') \
		.set_customer_ship_city('San Diego') \
		.set_customer_ship_state('CA') \
		.set_customer_ship_zip('92009') \
		.set_customer_ship_phone('6191231234') \
		.set_customer_ship_fax('6191234321') \
		.set_customer_ship_email('test@coolcommerce.net') \
		.set_customer_ship_country('USA') \
		.set_customer_ship_company('Miva Inc')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerUpdate)

	customer = helper.get_customer('CustomerUpdateTest_01')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_password_email() == 'test@coolcommerce.net'
	assert customer.get_bill_first_name() == 'John'
	assert customer.get_bill_last_name() == 'Doe'
	assert customer.get_bill_address1() == '1234 Some St'
	assert customer.get_bill_address2() == 'Unit 100'
	assert customer.get_bill_city() == 'San Diego'
	assert customer.get_bill_state() == 'CA'
	assert customer.get_bill_zip() == '92009'
	assert customer.get_bill_country() == 'USA'
	assert customer.get_bill_company() == 'Miva Inc'
	assert customer.get_bill_phone() == '6191231234'
	assert customer.get_bill_fax() == '6191234321'
	assert customer.get_bill_email() == 'test@coolcommerce.net'
	assert customer.get_ship_first_name() == 'John'
	assert customer.get_ship_last_name() == 'Deer'
	assert customer.get_ship_address1() == '4321 Some St'
	assert customer.get_ship_address2() == 'Unit 200'
	assert customer.get_ship_city() == 'San Diego'
	assert customer.get_ship_state() == 'CA'
	assert customer.get_ship_zip() == '92009'
	assert customer.get_ship_phone() == '6191231234'
	assert customer.get_ship_fax() == '6191234321'
	assert customer.get_ship_email() == 'test@coolcommerce.net'
	assert customer.get_ship_country() == 'USA'
	assert customer.get_ship_company() == 'Miva Inc'


def test_customer_payment_card_register():
	"""
	Tests the CustomerPaymentCard_Register API Call
	"""

	helper.provision_store('CustomerPaymentCard_Register.xml')

	customer_payment_card_register_test_register_card()


def customer_payment_card_register_test_register_card():
	request = merchantapi.request.CustomerPaymentCardRegister(helper.init_client())

	request.set_customer_login('CustomerPaymentCardRegisterTest')\
		.set_first_name('John')\
		.set_last_name('Doe')\
		.set_card_type('Visa')\
		.set_card_number('4111111111111111')\
		.set_expiration_month(8)\
		.set_expiration_year(2025)\
		.set_address1('1234 Test St')\
		.set_address2('Unit 123')\
		.set_city('San Diego')\
		.set_state('CA')\
		.set_zip('92009')\
		.set_country('US')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPaymentCardRegister)

	card = response.get_customer_payment_card()

	assert isinstance(card, merchantapi.model.CustomerPaymentCard)
	assert card.get_token() is not None
	assert card.get_first_name() == 'John'
	assert card.get_last_name() == 'Doe'
	assert card.get_type() == 'Visa'
	assert card.get_last_four() == '1111'
	assert card.get_expiration_month() == 8
	assert card.get_expiration_year() == 2025
	assert card.get_address1() == '1234 Test St'
	assert card.get_address2() == 'Unit 123'
	assert card.get_city() == 'San Diego'
	assert card.get_state() == 'CA'
	assert card.get_zip() == '92009'
	assert card.get_country() == 'US'


def test_module():
	"""
	Tests the Module API Call
	"""

	module_test_invalid_module()


def module_test_invalid_module():
	request = merchantapi.request.Module(helper.init_client())

	request.set_module_code('InvalidModule')\
		.set_module_function('InvalidModuleFunction')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.Module)


def test_note_list_load_query():
	"""
	Tests the NoteList_Load_Query API Call
	"""

	helper.provision_store('NoteList_Load_Query.xml')

	note_list_load_query_test_list_load()


def note_list_load_query_test_list_load():
	request = merchantapi.request.NoteListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
		.equal('cust_login', 'NoteListLoadQuery_Customer_1')
		.and_equal('order_id', 10520)
		.and_equal('business_title', 'NoteListLoadQuery_BusinessAccount_1')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteListLoadQuery)

	assert isinstance(response.get_notes(), list)
	assert len(response.get_notes()) == 6

	for note in response.get_notes():
		assert isinstance(note, merchantapi.model.Note)
		assert note.get_business_title() == 'NoteListLoadQuery_BusinessAccount_1'
		assert note.get_customer_login() == 'NoteListLoadQuery_Customer_1'
		assert note.get_order_id() == 10520
		assert note.get_note_text() == 'This note should be customer NoteListLoadQuery_Customer_1 and order 10520 and business NoteListLoadQuery_BusinessAccount_1'


def test_note_delete():
	"""
	Tests the Note_Delete API Call
	"""

	helper.provision_store('Note_Delete.xml')

	note_delete_test_deletion_by_business_account()
	note_delete_test_deletion_by_customer()


def note_delete_test_deletion_by_business_account():
	note = helper.get_note('business_title', 'NoteDeleteTest_BusinessAccount')

	assert isinstance(note, merchantapi.model.Note)

	request = merchantapi.request.NoteDelete(helper.init_client(), note)

	assert request.get_note_id() == note.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteDelete)


def note_delete_test_deletion_by_customer():
	note = helper.get_note('cust_login', 'NoteDeleteTest_Customer')

	assert isinstance(note, merchantapi.model.Note)

	request = merchantapi.request.NoteDelete(helper.init_client(), note)

	assert request.get_note_id() == note.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteDelete)


def test_note_insert():
	"""
	Tests the Note_Insert API Call
	"""

	helper.provision_store('Note_Insert.xml')

	note_insert_test_insertion_by_customer()
	note_insert_test_insertion_by_order()
	note_insert_test_invalid_customer()
	note_insert_test_invalid_order()


def note_insert_test_insertion_by_customer():
	customer = helper.get_customer('NoteInsertTest_Customer')

	assert isinstance(customer, merchantapi.model.Customer)

	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_customer_id(customer.get_id())\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteInsert)
	
	assert isinstance(response.get_note(), merchantapi.model.Note)
	assert response.get_note().get_note_text() == request.get_note_text()
	assert response.get_note().get_customer_id() == request.get_customer_id()


def note_insert_test_insertion_by_order():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_order_id(592745)\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteInsert)
	
	assert isinstance(response.get_note(), merchantapi.model.Note)
	assert response.get_note().get_note_text() == request.get_note_text()
	assert response.get_note().get_order_id() == request.get_order_id()


def note_insert_test_invalid_customer():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_customer_id(int(time.time()))\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.NoteInsert)


def note_insert_test_invalid_order():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_order_id(int(time.time()))\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.NoteInsert)


def test_note_update():
	"""
	Tests the Note_Update API Call
	"""

	helper.provision_store('Note_Update.xml')

	note_update_test_update()


def note_update_test_update():
	notes_request = merchantapi.request.NoteListLoadQuery(helper.init_client())

	notes_request.set_filters(
		notes_request.filter_expression()
		.equal('cust_login', 'NoteUpdateTest_Customer')
		.or_equal('business_title', 'NoteUpdateTest_BusinessAccount')
		.or_equal('order_id', 978375551)
	)

	notes_response = notes_request.send()

	helper.validate_response_success(notes_response, merchantapi.response.NoteListLoadQuery)

	notes = notes_response.get_notes()

	assert isinstance(notes, list)
	assert len(notes) > 2

	request = merchantapi.request.NoteUpdate(helper.init_client())
	note_text = 'New Note Text %d' % int(time.time())

	request.set_note_id(notes[0].get_id())\
		.set_note_text(note_text)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteUpdate)

	note = helper.get_note('id', notes[0].get_id())

	assert isinstance(note, merchantapi.model.Note)
	assert note.get_note_text() == note_text


def test_order_custom_field_list_load():
	"""
	Tests the OrderCustomFieldList_Load API Call
	"""

	helper.provision_store('OrderCustomFieldList_Load.xml')

	order_custom_field_list_load_test_list_load()


def order_custom_field_list_load_test_list_load():
	request = merchantapi.request.OrderCustomFieldListLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCustomFieldListLoad)

	assert isinstance(response.get_order_custom_fields(), list)
	assert len(response.get_order_custom_fields()) > 1

	for ocf in response.get_order_custom_fields():
		assert isinstance(ocf, merchantapi.model.OrderCustomField)


def test_order_custom_fields_update():
	"""
	Tests the OrderCustomFields_Update API Call
	"""

	helper.provision_store('OrderCustomFields_Update.xml')

	order_custom_fields_update_test_update()


def order_custom_fields_update_test_update():
	request = merchantapi.request.OrderCustomFieldsUpdate(helper.init_client())

	request.set_order_id(65191651)

	request.get_custom_field_values()\
		.add_value('OrderCustomFieldsUpdate_Field_1', 'foobar')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCustomFieldsUpdate)

	order = helper.get_order(65191651)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert order.get_custom_field_values().get_value('OrderCustomFieldsUpdate_Field_1') == 'foobar'


def test_order_item_list_back_order():
	"""
	Tests the OrderItemList_BackOrder API Call
	"""

	helper.provision_store('OrderItemList_BackOrder.xml')

	order_item_list_back_order_test_backorder()
	order_item_list_back_order_test_add_items_from_orderitem_instance()


def order_item_list_back_order_test_backorder():
	order = helper.get_order(678566)

	assert isinstance(order, merchantapi.model.Order)

	isdate = int(time.time()) + int(random.random() + 1000)

	request = merchantapi.request.OrderItemListBackOrder(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	request.set_date_in_stock(isdate)

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	assert len(order.get_items()) == len(request.get_line_ids())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListBackOrder)

	checkorder = helper.get_order(678566)

	assert isinstance(checkorder, merchantapi.model.Order)
	assert checkorder.get_date_in_stock() == isdate

	for item in checkorder.get_items():
		assert item.get_status() == merchantapi.model.OrderItem.ORDER_ITEM_STATUS_BACKORDERED


def order_item_list_back_order_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListBackOrder(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines


def test_order_item_list_cancel():
	"""
	Tests the OrderItemList_Cancel API Call
	"""

	helper.provision_store('OrderItemList_Cancel.xml')

	order_item_list_cancel_test_cancel()
	order_item_list_cancel_test_add_items_from_orderitem_instance()


def order_item_list_cancel_test_cancel():
	order = helper.get_order(678567)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 4

	request = merchantapi.request.OrderItemListCancel(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	request.set_reason('API Test')

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCancel)

	order = helper.get_order(678567)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 4

	for item in order.get_items():
		assert isinstance(item, merchantapi.model.OrderItem)
		assert item.get_status() == merchantapi.model.OrderItem.ORDER_ITEM_STATUS_CANCELLED
		assert isinstance(item.get_options(), list)
		assert len(item.get_options()) == 1
		assert item.get_options()[0].get_attribute_code() == 'Cancellation Reason'
		assert item.get_options()[0].get_value() == 'API Test'


def order_item_list_cancel_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListCancel(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines


def test_order_item_list_create_shipment():
	"""
	Tests the OrderItemList_CreateShipment API Call
	"""

	helper.provision_store('OrderItemList_CreateShipment.xml')

	order_item_list_create_shipment_test_create_shipment()
	order_item_list_create_shipment_test_add_items_from_orderitem_instance()


def order_item_list_create_shipment_test_create_shipment():
	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)

	request = merchantapi.request.OrderItemListCreateShipment(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCreateShipment)

	assert isinstance(response.get_order_shipment(), merchantapi.model.OrderShipment)
	assert order.get_id() == response.get_order_shipment().get_order_id()
	assert response.get_order_shipment().get_id() > 0


def order_item_list_create_shipment_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListCreateShipment(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines


def test_order_item_list_delete():
	"""
	Tests the OrderItemList_Delete API Call
	"""

	helper.provision_store('OrderItemList_Delete.xml')

	order_item_list_delete_test_deletion()
	order_item_list_delete_test_add_items_from_orderitem_instance()


def order_item_list_delete_test_deletion():
	order = helper.get_order(678568)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 4

	request = merchantapi.request.OrderItemListDelete(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListDelete)

	order = helper.get_order(678568)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 0


def order_item_list_delete_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListDelete(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines


def test_order_item_add():
	"""
	Tests the OrderItem_Add API Call
	"""

	helper.provision_store('OrderItem_Add.xml')

	order_item_add_test_insertion()
	order_item_add_test_add_product()
	order_item_add_test_add_product_with_option()
	order_item_add_test_insertion_with_attribute()
	order_item_add_test_insertion_with_invalid_attribute()


def order_item_add_test_insertion():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678565)\
		.set_code('OrderItemAddTest_Foo')\
		.set_quantity(2)\
		.set_price(10.00)\
		.set_taxable(True)\
		.set_weight(1.00)\
		.set_sku('OrderItemAddTest_Foo_SKU')\
		.set_name('OrderItemAddTest - Foo')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 20.00
	assert response.get_order_total_and_item().get_formatted_total() == '$20.00'
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_code() == 'OrderItemAddTest_Foo'
	assert response.get_order_total_and_item().get_order_item().get_quantity() == 2
	assert response.get_order_total_and_item().get_order_item().get_price() == 10.00
	assert response.get_order_total_and_item().get_order_item().get_weight() == 1.00
	assert response.get_order_total_and_item().get_order_item().get_sku() == 'OrderItemAddTest_Foo_SKU'
	assert response.get_order_total_and_item().get_order_item().get_name() == 'OrderItemAddTest - Foo'

	order = helper.get_order(678565)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert item.get_line_id() == response.get_order_total_and_item().get_order_item().get_line_id()


def order_item_add_test_add_product():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678566) \
		.set_code('OrderItemAddTest_Product') \
		.set_quantity(1) \
		.set_price(9.99) \
		.set_name('OrderItemAddTest_Product')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 9.99
	assert response.get_order_total_and_item().get_formatted_total() == '$9.99'

	order = helper.get_order(678566)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert item.get_code() == 'OrderItemAddTest_Product'
	assert item.get_quantity() == 1
	assert item.get_name() == 'OrderItemAddTest_Product'


def order_item_add_test_add_product_with_option():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678567) \
		.set_code('OrderItemAddTest_Product_2') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_Product_2')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('color')\
		.set_value('red')

	request.add_option(option)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 12.99
	assert response.get_order_total_and_item().get_formatted_total() == '$12.99'


def order_item_add_test_insertion_with_attribute():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678568) \
		.set_code('OrderItemAddTest_ItemWOptions') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_ItemWOptions')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('foo')\
		.set_value('bar')\
		.set_price(3.29)\
		.set_weight(1.25)

	request.add_option(option)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 16.28
	assert response.get_order_total_and_item().get_formatted_total() == '$16.28'


def order_item_add_test_insertion_with_invalid_attribute():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678568) \
		.set_code('OrderItemAddTest_ItemWOptions') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_ItemWOptions')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('')\
		.set_value('')

	request.add_option(option)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemAdd)


def test_order_item_update():
	"""
	Tests the OrderItem_Update API Call
	"""

	helper.provision_store('OrderItem_Update.xml')

	order_item_update_test_update()
	order_item_update_test_update_with_existing_attribute()


def order_item_update_test_update():
	order = helper.get_order(678569)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 2

	item1 = order.get_items()[0]

	request = merchantapi.request.OrderItemUpdate(helper.init_client(), item1)

	assert request.get_line_id() == item1.get_line_id()

	request.set_order_id(order.get_id())\
		.set_line_id(item1.get_line_id())\
		.set_quantity(item1.get_quantity() + 1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemUpdate)


def order_item_update_test_update_with_existing_attribute():
	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item1 = order.get_items()[0]

	request = merchantapi.request.OrderItemUpdate(helper.init_client(), item1)

	assert request.get_line_id() == item1.get_line_id()
	assert isinstance(item1.get_options(), list)
	assert len(item1.get_options()) == 1
	assert isinstance(item1.get_options()[0], merchantapi.model.OrderItemOption)

	request.set_order_id(order.get_id())\
		.set_line_id(item1.get_line_id())\
		.set_quantity(item1.get_quantity() + 2)

	request.get_options()[0].set_value('BIN')\
		.set_price(29.99)\
		.set_weight(15.00)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemUpdate)

	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert isinstance(item.get_options(), list)
	assert len(item.get_options()) == 1

	option = item.get_options()[0]

	assert isinstance(option, merchantapi.model.OrderItemOption)
	assert option.get_price() == 29.99
	assert option.get_weight() == 15.00


def test_order_list_load_query():
	"""
	Tests the OrderList_Load_Query API Call
	"""

	helper.provision_store('OrderList_Load_Query.xml')
	helper.upload_image('graphics/OrderListLoadQuery1.jpg')
	helper.upload_image('graphics/OrderListLoadQuery2.jpg')
	helper.upload_image('graphics/OrderListLoadQuery3.jpg')
	helper.upload_image('graphics/OrderListLoadQuery4.jpg')
	helper.upload_image('graphics/OrderListLoadQuery5.jpg')
	helper.upload_image('graphics/OrderListLoadQuery6.jpg')
	helper.upload_image('graphics/OrderListLoadQuery7.jpg')

	order_list_load_query_test_list_load()
	order_list_load_query_test_list_load_with_custom_fields()
	order_list_load_query_test_list_load_detailed()
	order_list_load_query_test_list_load_MMAPI61()


def order_list_load_query_test_list_load():
	request = merchantapi.request.OrderListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().equal('cust_login', 'OrderListLoadQueryTest_Cust1')) \
		.add_on_demand_column('cust_login')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderListLoadQuery)

	assert isinstance(response.get_orders(), list)
	assert len(response.get_orders()) == 7

	for order in response.get_orders():
		assert isinstance(order, merchantapi.model.Order)
		assert order.get_customer_login() == 'OrderListLoadQueryTest_Cust1'
		assert order.get_id() in [678571, 678572, 678573, 678574, 678575, 678576, 678577]


def order_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.OrderListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().equal('cust_login', 'OrderListLoadQueryTest_Cust1')) \
		.set_on_demand_columns([
			'ship_method',
			'cust_login',
			'cust_pw_email',
			'business_title',
			'payment_module',
			'customer',
			'items',
			'charges',
			'coupons',
			'discounts',
			'payments',
			'notes'
		]) \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_checkbox') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_imageupload') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_text') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_textarea') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_dropdown')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderListLoadQuery)

	assert isinstance(response.get_orders(), list)
	assert len(response.get_orders()) == 7

	for i, order in enumerate(response.get_orders()):
		assert isinstance(order, merchantapi.model.Order)
		assert order.get_customer_login() == 'OrderListLoadQueryTest_Cust1'
		assert order.get_id() in [678571, 678572, 678573, 678574, 678575, 678576, 678577]
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_checkbox', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_checkbox', 'customfields') == '1'
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_imageupload', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/OrderListLoadQuery%d.jpg' % int(i+1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_text', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_text', 'customfields') == 'OrderListLoadQueryTest_%d' % int(i + 1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_textarea', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_textarea', 'customfields') == 'OrderListLoadQueryTest_%d' % int(i + 1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_dropdown', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i + 1)



def order_list_load_query_test_list_load_detailed():
	cod = helper.get_module('cod')
	assert cod is not None

	order = helper.get_order(678578)

	assert order is not None

	auth_response = helper.send_admin_request('Order_Authorize', {
        'Order_ID': 	order.get_id(),
        'Module_ID': 	cod['id'],
        'Amount': 		order.get_total(),
        'Module_Data': 	''
	})

	auth_response_data = json.loads(auth_response.content)

	assert auth_response_data is not None
	assert auth_response_data['success']

	order = helper.get_order(order.get_id())

	assert order is not None
    
	expected_charge_types = [ 'CUSTOM', 'SHIPPING', 'DISCOUNT', 'TAX' ]
	expected_discounts = [ 'OrderListLoadQueryTestDetailed_1', 'OrderListLoadQueryTestDetailed_2' ]

	assert len(order.get_items()) == 1
	assert order.get_items()[0].get_code() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_items()[0].get_name() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_items()[0].get_line_id() > 0
	assert order.get_items()[0].get_price() == 52.24
	assert order.get_items()[0].get_quantity() == 1
	assert order.get_items()[0].get_retail() == 5.0
	assert order.get_items()[0].get_order_id() == order.get_id()

	assert len(order.get_coupons()) == 1
	assert order.get_coupons()[0].get_code() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_coupons()[0].get_total() == 2.75
	assert order.get_coupons()[0].get_coupon_id() > 0
	assert order.get_coupons()[0].get_order_id() == order.get_id()

	assert len(order.get_charges()) == 4
	for charge in order.get_charges():
		assert charge.get_type() in expected_charge_types
		if charge.get_type() == 'CUSTOM':
			assert charge.get_amount() == 1.00
			assert charge.get_formatted_amount() == '$1.00'
			assert charge.get_charge_id() > 0
			assert charge.get_order_id() == order.get_id()


	assert len(order.get_discounts()) == 2
	for discount in order.get_discounts():
		assert discount.get_name() in expected_discounts
		assert discount.get_order_id() == order.get_id()

	assert len(order.get_payments()) == 1
	assert order.get_payments()[0].get_amount() == 60.73
	assert order.get_payments()[0].get_available() == 60.73
	assert order.get_payments()[0].get_formatted_amount() == '$60.73'
	assert order.get_payments()[0].get_formatted_available() == '$60.73'
	assert order.get_payments()[0].get_id() > 0
	assert order.get_payments()[0].get_order_id() == order.get_id()
	assert order.get_payments()[0].get_expires() == 0


def order_list_load_query_test_list_load_MMAPI61():
	order = helper.get_order(678578)

	assert order is not None
	assert len(order.get_items()) == 1
	assert len(order.get_items()[0].get_discounts()) > 0


def test_order_shipment_list_update():
	"""
	Tests the OrderShipmentList_Update API Call
	"""

	helper.provision_store('OrderShipmentList_Update.xml')

	order_shipment_list_update_test_update()


def order_shipment_list_update_test_update():
	request = merchantapi.request.OrderShipmentListUpdate(helper.init_client())
	update = merchantapi.model.OrderShipmentUpdate()

	update.set_cost(1.00) \
		.set_mark_shipped(True) \
		.set_shipment_id(100) \
		.set_tracking_number('Z12312312313') \
		.set_tracking_type('UPS')

	request.add_shipment_update(update)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListUpdate)


def test_order_create():
	"""
	Tests the Order_Create API Call
	"""

	helper.provision_store('Order_Create.xml')

	order_create_test_creation()
	order_create_test_creation_with_customer()
	order_create_test_invalid_customer()
	order_create_test_with_customer_info()
	order_create_test_creation_with_everything()


def order_create_test_creation():
	request = merchantapi.request.OrderCreate(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0


def order_create_test_creation_with_customer():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_customer_login('OrderCreateTest_Cust_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_customer_id() > 0


def order_create_test_invalid_customer():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_customer_login('InvalidCustomer')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderCreate)


def order_create_test_with_customer_info():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_ship_first_name('Joe') \
		.set_ship_last_name('Dirt') \
		.set_ship_email('test@coolcommerce.net') \
		.set_ship_phone('6191231234') \
		.set_ship_fax('6191234321') \
		.set_ship_company('Dierte Inc') \
		.set_ship_address1('1234 Test Ave') \
		.set_ship_address2('Unit 100') \
		.set_ship_city('San Diego') \
		.set_ship_state('CA') \
		.set_ship_zip('92009') \
		.set_ship_country('USA') \
		.set_ship_residential(True) \
		.set_bill_first_name('Joe') \
		.set_bill_last_name('Dirt') \
		.set_bill_email('test@coolcommerce.net') \
		.set_bill_phone('6191231234') \
		.set_bill_fax('6191234321') \
		.set_bill_company('Dierte Inc') \
		.set_bill_address1('1234 Test Ave') \
		.set_bill_address2('Unit 100') \
		.set_bill_city('San Diego') \
		.set_bill_state('CA') \
		.set_bill_zip('92009') \
		.set_bill_country('US') \
		.set_calculate_charges(False) \
		.set_trigger_fulfillment_modules(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_ship_first_name() == 'Joe'
	assert response.get_order().get_ship_last_name() == 'Dirt'
	assert response.get_order().get_ship_email() == 'test@coolcommerce.net'
	assert response.get_order().get_ship_phone() == '6191231234'
	assert response.get_order().get_ship_fax() == '6191234321'
	assert response.get_order().get_ship_company() == 'Dierte Inc'
	assert response.get_order().get_ship_address1() == '1234 Test Ave'
	assert response.get_order().get_ship_address2() == 'Unit 100'
	assert response.get_order().get_ship_city() == 'San Diego'
	assert response.get_order().get_ship_state() == 'CA'
	assert response.get_order().get_ship_zip() == '92009'
	assert response.get_order().get_ship_country() == 'USA'
	assert response.get_order().get_ship_residential() is True
	assert response.get_order().get_bill_first_name() == 'Joe'
	assert response.get_order().get_bill_last_name() == 'Dirt'
	assert response.get_order().get_bill_email() == 'test@coolcommerce.net'
	assert response.get_order().get_bill_phone() == '6191231234'
	assert response.get_order().get_bill_fax() == '6191234321'
	assert response.get_order().get_bill_company() == 'Dierte Inc'
	assert response.get_order().get_bill_address1() == '1234 Test Ave'
	assert response.get_order().get_bill_address2() == 'Unit 100'
	assert response.get_order().get_bill_city() == 'San Diego'
	assert response.get_order().get_bill_state() == 'CA'
	assert response.get_order().get_bill_zip() == '92009'
	assert response.get_order().get_bill_country() == 'US'


def order_create_test_creation_with_everything():
	request = merchantapi.request.OrderCreate(helper.init_client())
	charge = merchantapi.model.OrderCharge()
	item = merchantapi.model.OrderItem()
	item_opt = merchantapi.model.OrderItemOption()
	product = merchantapi.model.OrderProduct()
	prod_attr = merchantapi.model.OrderProductAttribute()

	charge.set_description('foo') \
		.set_amount(29.99) \
		.set_type('API')

	item.set_name('Test Custom Line') \
		.set_code('CUSTOM_LINE') \
		.set_price(15.00) \
		.set_quantity(1)

	item_opt.set_attribute_code('option')\
		.set_value('option_data') \
		.set_price(5.00) \
		.set_weight(1.00)

	item.add_option(item_opt)

	product.set_code('OrderCreateTest_Prod_3') \
		.set_quantity(1)

	prod_attr.set_code('color') \
		.set_value('red')

	product.add_attribute(prod_attr)

	request.set_customer_login('OrderCreateTest_Cust_2') \
		.set_calculate_charges(False) \
		.set_trigger_fulfillment_modules(False) \
		.add_charge(charge) \
		.add_item(item) \
		.add_product(product)

	request.get_custom_field_values() \
		.add_value('OrderCreateTest_1', 'foo') \
		.add_value('OrderCreateTest_2', 'bar') \
		.add_value('OrderCreateTest_3', 'baz', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0

	order = helper.get_order(response.get_order().get_id())

	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() == response.get_order().get_id()
	assert order.get_customer_login() == 'OrderCreateTest_Cust_2'
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 2

	item1 = order.get_items()[0]

	assert item1.get_code() == 'CUSTOM_LINE'
	assert item1.get_price() == 15.00
	assert isinstance(item1.get_options(), list)
	assert len(item1.get_options()) == 1

	item1_option1 = item1.get_options()[0]

	assert item1_option1.get_attribute_code() == 'option'
	assert item1_option1.get_value() == 'option_data'
	assert item1_option1.get_price() == 5.00
	assert item1_option1.get_weight() == 1.00

	item2 = order.get_items()[1]

	assert item2.get_code() == 'OrderCreateTest_Prod_3'
	assert item2.get_price() == 4.00
	assert isinstance(item2.get_options(), list)
	assert len(item2.get_options()) == 1

	item2_option1 = item2.get_options()[0]

	assert item2_option1.get_attribute_code() == 'color'
	assert item2_option1.get_value() == 'red'
	assert item2_option1.get_price() == 5.99
	assert item2_option1.get_weight() == 1.21

	assert isinstance(order.get_charges(), list)
	assert len(order.get_charges()) == 1

	charge = order.get_charges()[0]

	assert isinstance(charge, merchantapi.model.OrderCharge)
	assert charge.get_description() == 'foo'
	assert charge.get_amount() == 29.99
	assert charge.get_type() == 'API'

	assert isinstance(order.get_customer(), merchantapi.model.Customer)
	assert order.get_customer().get_login() == 'OrderCreateTest_Cust_2'
	assert isinstance(order.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert order.get_custom_field_values().get_value('OrderCreateTest_1') == 'foo'
	assert order.get_custom_field_values().get_value('OrderCreateTest_2') == 'bar'
	assert order.get_custom_field_values().get_value('OrderCreateTest_3') == 'baz'


def test_order_delete():
	"""
	Tests the Order_Delete API Call
	"""

	order_delete_test_deletion()


def order_delete_test_deletion():
	createrequest = merchantapi.request.OrderCreate(helper.init_client())

	createresponse = createrequest.send()

	helper.validate_response_success(createresponse, merchantapi.response.OrderCreate)

	assert isinstance(createresponse.get_order(), merchantapi.model.Order)
	assert createresponse.get_order().get_id() > 0

	request = merchantapi.request.OrderDelete(helper.init_client(), createresponse.get_order())

	assert request.get_order_id() == createresponse.get_order().get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderDelete)


def test_order_update_customer_information():
	"""
	Tests the Order_Update_Customer_Information API Call
	"""

	helper.provision_store('Order_Update_Customer_Information.xml')

	order_update_customer_information_test_update()


def order_update_customer_information_test_update():
	order = helper.get_order(678571)
	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() > 0

	request = merchantapi.request.OrderUpdateCustomerInformation(helper.init_client())

	request.set_order_id(order.get_id()) \
		.set_ship_first_name('Joe') \
		.set_ship_last_name('Dirt') \
		.set_ship_email('test@coolcommerce.net') \
		.set_ship_phone('6191231234') \
		.set_ship_fax('6191234321') \
		.set_ship_company('Dierte Inc') \
		.set_ship_address1('1234 Test Ave') \
		.set_ship_address2('Unit 100') \
		.set_ship_city('San Diego') \
		.set_ship_state('CA') \
		.set_ship_zip('92009') \
		.set_ship_country('USA') \
		.set_ship_residential(True) \
		.set_bill_first_name('Joe') \
		.set_bill_last_name('Dirt') \
		.set_bill_email('test@coolcommerce.net') \
		.set_bill_phone('6191231234') \
		.set_bill_fax('6191234321') \
		.set_bill_company('Dierte Inc') \
		.set_bill_address1('1234 Test Ave') \
		.set_bill_address2('Unit 100') \
		.set_bill_city('San Diego') \
		.set_bill_state('CA') \
		.set_bill_zip('92009') \
		.set_bill_country('US')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderUpdateCustomerInformation)

	checkorder = helper.get_order(678571)

	assert isinstance(checkorder, merchantapi.model.Order)
	assert order.get_ship_first_name() != checkorder.get_ship_first_name()
	assert order.get_ship_last_name() != checkorder.get_ship_last_name()
	assert order.get_ship_phone() != checkorder.get_ship_phone()
	assert order.get_ship_fax() != checkorder.get_ship_fax()
	assert order.get_ship_city() != checkorder.get_ship_city()
	assert order.get_ship_state() != checkorder.get_ship_state()
	assert order.get_ship_zip() != checkorder.get_ship_zip()
	assert order.get_ship_country() != checkorder.get_ship_country()
	assert order.get_ship_address1() != checkorder.get_ship_address1()
	assert order.get_ship_address2() != checkorder.get_ship_address2()
	assert order.get_bill_first_name() != checkorder.get_bill_first_name()
	assert order.get_bill_last_name() != checkorder.get_bill_last_name()
	assert order.get_bill_phone() != checkorder.get_bill_phone()
	assert order.get_bill_fax() != checkorder.get_bill_fax()
	assert order.get_bill_city() != checkorder.get_bill_city()
	assert order.get_bill_state() != checkorder.get_bill_state()
	assert order.get_bill_zip() != checkorder.get_bill_zip()
	assert order.get_bill_country() != checkorder.get_bill_country()
	assert order.get_bill_address1() != checkorder.get_bill_address1()
	assert order.get_bill_address2() != checkorder.get_bill_address2()


def test_price_group_customer_update_assigned():
	"""
	Tests the PriceGroupCustomer_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupCustomer_Update_Assigned.xml')

	price_group_customer_update_assigned_test_assignment()
	price_group_customer_update_assigned_test_unassignment()
	price_group_customer_update_assigned_test_invalid_assign()
	price_group_customer_update_assigned_test_invalid_price_group()
	price_group_customer_update_assigned_test_invalid_customer()


def price_group_customer_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupCustomerUpdateAssigned(helper.init_client())

	request.set_customer_login('PriceGroupCustomerUpdateAssignedTest_01')\
		.set_price_group_name('PriceGroupCustomerUpdateAssignedTest')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCustomerUpdateAssigned)


def price_group_customer_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupCustomerUpdateAssigned(helper.init_client())

	request.set_customer_login('PriceGroupCustomerUpdateAssignedTest_01')\
		.set_price_group_name('PriceGroupCustomerUpdateAssignedTest')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCustomerUpdateAssigned)


def price_group_customer_update_assigned_test_invalid_assign():
	request = merchantapi.request.PriceGroupCustomerUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_customer_login('PriceGroupCustomerUpdateAssignedTest_01')\
		.set_price_group_name('PriceGroupCustomerUpdateAssignedTest')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupCustomerUpdateAssigned)


def price_group_customer_update_assigned_test_invalid_price_group():
	request = merchantapi.request.PriceGroupCustomerUpdateAssigned(helper.init_client())

	request.set_customer_login('PriceGroupCustomerUpdateAssignedTest_01')\
		.set_price_group_name('InvalidPriceGroup')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupCustomerUpdateAssigned)


def price_group_customer_update_assigned_test_invalid_customer():
	request = merchantapi.request.PriceGroupCustomerUpdateAssigned(helper.init_client())

	request.set_customer_login('InvalidCustomer')\
		.set_price_group_name('PriceGroupCustomerUpdateAssignedTest')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupCustomerUpdateAssigned)


def test_price_group_list_load_query():
	"""
	Tests the PriceGroupList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupList_Load_Query.xml')

	price_group_list_load_query_test_list_load()


def price_group_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('name', 'PriceGroupListLoadQueryTest_%')) \
		.set_sort('id', merchantapi.request.PriceGroupListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupListLoadQuery)

	assert isinstance(response.get_price_groups(), list)
	assert len(response.get_price_groups()) == 14

	for i, pg in enumerate(response.get_price_groups()):
		assert isinstance(pg, merchantapi.model.PriceGroup)
		assert pg.get_name() == 'PriceGroupListLoadQueryTest_%d' % int(i+1)


def test_price_group_product_update_assigned():
	"""
	Tests the PriceGroupProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupProduct_Update_Assigned.xml')

	price_group_product_update_assigned_test_assignment()
	price_group_product_update_assigned_test_unassignment()
	price_group_product_update_assigned_test_invalid_assign()
	price_group_product_update_assigned_test_invalid_price_group()
	price_group_product_update_assigned_test_invalid_product()


def price_group_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_price_group():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('InvalidPriceGroup')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_product():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('InvalidProduct')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def test_product_image_add():
	"""
	Tests the ProductImage_Add API Call
	"""

	helper.upload_image('graphics/ProductImageAdd.jpg')
	helper.provision_store('ProductImage_Add.xml')

	product_image_add_test_add()
	product_image_add_test_invalid_product()
	product_image_add_test_invalid_product_path()


def product_image_add_test_add():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('ProductImageAddTest') \
		.set_filepath('graphics/00000001/1/ProductImageAdd.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductImageAdd)
	assert isinstance(response.get_product_image_data(), merchantapi.model.ProductImageData)
	assert response.get_product_image_data().get_id() > 0


def product_image_add_test_invalid_product():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('InvalidProductImageAddTest') \
		.set_filepath('graphics/00000001/1/ProductImageAdd.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductImageAdd)


def product_image_add_test_invalid_product_path():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('ProductImageAddTest') \
		.set_filepath('graphics/00000001/InvalidImage.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductImageAdd)


def test_product_image_delete():
	"""
	Tests the ProductImage_Delete API Call
	"""

	helper.provision_store('ProductImage_Delete_Cleanup_v10.xml')
	helper.upload_image('graphics/ProductImageDelete.jpg')
	helper.provision_store('ProductImage_Delete_v10.xml')

	product_image_delete_test_deletion()


def product_image_delete_test_deletion():
	product = helper.get_product('ProductImageDeleteTest')

	assert isinstance(product, merchantapi.model.Product)
	assert isinstance(product.get_product_image_data(), list)
	assert len(product.get_product_image_data()) == 1

	request = merchantapi.request.ProductImageDelete(helper.init_client(), product.get_product_image_data()[0])

	assert request.get_product_image_id() == product.get_product_image_data()[0].get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductImageDelete)


def test_product_list_adjust_inventory():
	"""
	Tests the ProductList_Adjust_Inventory API Call
	"""

	helper.provision_store('ProductList_Adjust_Inventory.xml')

	product_list_adjust_inventory_test_adjustment()


def product_list_adjust_inventory_test_adjustment():
	product = helper.get_product('ProductListAdjustInventoryTest_1')

	request = merchantapi.request.ProductListAdjustInventory(helper.init_client())
	adjustment = merchantapi.model.ProductInventoryAdjustment()

	adjustment.set_product_id(product.get_id()) \
		.set_adjustment(100)

	request.add_inventory_adjustment(adjustment)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListAdjustInventory)


def test_product_list_load_query():
	"""
	Tests the ProductList_Load_Query API Call
	"""

	helper.upload_image('graphics/ProductListLoadQuery1.jpg')
	helper.upload_image('graphics/ProductListLoadQuery2.jpg')
	helper.upload_image('graphics/ProductListLoadQuery3.jpg')
	helper.upload_image('graphics/ProductListLoadQuery4.jpg')
	helper.upload_image('graphics/ProductListLoadQuery5.jpg')
	helper.upload_image('graphics/ProductListLoadQuery6.jpg')
	helper.upload_image('graphics/ProductListLoadQuery7.jpg')
	helper.provision_store('ProductList_Load_Query_v10.xml')

	product_list_load_query_test_list_load()
	product_list_load_query_test_list_load_with_custom_fields()
	product_list_load_query_test_list_load_imagetypes()


def product_list_load_query_test_list_load():
	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
		.like('code', 'ProductListLoadQueryTest_%')
		.and_not_like('code', 'ProductListLoadQueryTest_Rel_%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert isinstance(response.get_products(), list)
	assert len(response.get_products()) == 7

	for i, product in enumerate(response.get_products()):
		assert isinstance(product, merchantapi.model.Product)
		assert product.get_code() == 'ProductListLoadQueryTest_%d' % int(i+1)
		assert product.get_price() == 2.00
		assert product.get_cost() == 1.00
		assert product.get_weight() == 1.00
		assert product.get_active() is False
		assert product.get_taxable() is False


def product_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ProductListLoadQueryTest_%')
			.and_not_like('code', 'ProductListLoadQueryTest_Rel_%')
	)

	request.set_on_demand_columns(request.get_available_on_demand_columns()) \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_checkbox') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_imageupload') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_text') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_textarea') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_dropdown') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_multitext')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert isinstance(response.get_products(), list)
	assert len(response.get_products()) == 7

	for i, product in enumerate(response.get_products()):
		assert isinstance(product, merchantapi.model.Product)
		assert product.get_code() == 'ProductListLoadQueryTest_%d' % int(i+1)
		assert product.get_price() == 2.00
		assert product.get_cost() == 1.00
		assert product.get_weight() == 1.00
		assert product.get_active() is False
		assert product.get_taxable() is False

		if product.get_code() in ['ProductListLoadQueryTest_1', 'ProductListLoadQueryTest_2']:
			assert isinstance(product.get_attributes(), list)
			assert len(product.get_attributes()) > 0

			for attribute in product.get_attributes():
				assert isinstance(attribute, merchantapi.model.ProductAttribute)

				if attribute.get_type() == 'select':
					assert isinstance(attribute.get_options(), list)
					assert len(attribute.get_options()) > 0

					for option in attribute.get_options():
						assert isinstance(option, merchantapi.model.ProductOption)

		assert isinstance(product.get_related_products(), list)
		assert len(product.get_related_products()) > 0

		for related in product.get_related_products():
			assert isinstance(related, merchantapi.model.RelatedProduct)
			assert related.get_code() in [
				'ProductListLoadQueryTest_Rel_1',
				'ProductListLoadQueryTest_Rel_2',
				'ProductListLoadQueryTest_Rel_3',
				'ProductListLoadQueryTest_Rel_4',
				'ProductListLoadQueryTest_Rel_5',
				'ProductListLoadQueryTest_Rel_6',
				'ProductListLoadQueryTest_Rel_7'
			]

		assert isinstance(product.get_categories(), list)
		assert len(product.get_categories()) > 0

		for category in product.get_categories():
			assert isinstance(category, merchantapi.model.Category)
			assert category.get_code() in [
				'ProductListLoadQueryTest_1',
				'ProductListLoadQueryTest_2',
				'ProductListLoadQueryTest_3',
				'ProductListLoadQueryTest_4',
				'ProductListLoadQueryTest_5',
				'ProductListLoadQueryTest_6',
				'ProductListLoadQueryTest_7'
			]

		assert isinstance(product.get_product_image_data(), list)
		assert len(product.get_product_image_data()) > 0

		for imagedata in product.get_product_image_data():
			assert isinstance(imagedata, merchantapi.model.ProductImageData)
			assert imagedata.get_image() in [
				'graphics/00000001/1/ProductListLoadQuery1.jpg',
				'graphics/00000001/1/ProductListLoadQuery2.jpg',
				'graphics/00000001/1/ProductListLoadQuery3.jpg',
				'graphics/00000001/1/ProductListLoadQuery4.jpg',
				'graphics/00000001/1/ProductListLoadQuery5.jpg',
				'graphics/00000001/1/ProductListLoadQuery6.jpg',
				'graphics/00000001/1/ProductListLoadQuery7.jpg'
			]

		assert isinstance(product.get_custom_field_values(), merchantapi.model.CustomFieldValues)
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_checkbox', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_imageupload', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_text', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_textarea', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_dropdown', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_multitext', 'customfields') is True


def product_list_load_query_test_list_load_imagetypes():
	types = [ 'PLLQ_ImageTypes_1', 'PLLQ_ImageTypes_2', 'PLLQ_ImageTypes_3' ]

	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.filters.equal('code', 'PLLQ_ImageTypes_1')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_1')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_2')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_3')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert len(response.get_products()) == 1
	assert len(response.get_products()[0].get_image_types()) == 3

	for (code,id) in response.get_products()[0].get_image_types().items():
		assert code in types


def test_product_variant_list_load_product():
	"""
	Tests the ProductVariantList_Load_Product API Call
	"""

	helper.provision_store('ProductVariantList_Load_Product.xml')

	product_variant_list_load_product_test_load()


def product_variant_list_load_product_test_load():
	request = merchantapi.request.ProductVariantListLoadProduct(helper.init_client())

	request.set_edit_product('ProductVariantListLoadProduct') \
		.set_include_default_variant(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListLoadProduct)

	assert isinstance(response.get_product_variants(), list)
	assert len(response.get_product_variants()) == 48

	for pv in response.get_product_variants():
		assert isinstance(pv, merchantapi.model.ProductVariant)
		assert isinstance(pv.get_parts(), list)
		assert len(pv.get_parts()) == 2

		for part in pv.get_parts():
			assert isinstance(part, merchantapi.model.ProductVariantPart)
			assert part.get_product_id() > 0
			assert 'PVLLP_' in part.get_product_code()

		assert isinstance(pv.get_dimensions(), list)
		assert len(pv.get_dimensions()) > 3

		for dimension in pv.get_dimensions():
			assert isinstance(dimension, merchantapi.model.ProductVariantDimension)
			assert dimension.get_attribute_id() > 0


def test_product_insert():
	"""
	Tests the Product_Insert API Call
	"""

	helper.provision_store('Product_Insert.xml')
	helper.upload_image('graphics/ProductInsert.jpg')

	product_insert_test_insertion()
	product_insert_test_insertion_with_custom_fields()
	product_insert_test_duplicate()


def product_insert_test_insertion():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_1') \
		.set_product_sku('ProductInsertTest_1_Sku') \
		.set_product_name('API Inserted Product 1') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductInsert)

	product = helper.get_product('ProductInsertTest_1')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductInsertTest_1'
	assert product.get_sku() == 'ProductInsertTest_1_Sku'
	assert product.get_name() == 'API Inserted Product 1'
	assert product.get_price() == 7.50
	assert product.get_cost() == 7.50
	assert product.get_id() > 0


def product_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_2') \
		.set_product_sku('ProductInsertTest_2_Sku') \
		.set_product_name('API Inserted Product 2') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	request.get_custom_field_values() \
		.add_value('ProductInsertTest_checkbox', 'True', 'customfields') \
		.add_value('ProductInsertTest_imageupload', 'graphics/00000001/ProductInsert.jpg', 'customfields') \
		.add_value('ProductInsertTest_text', 'ProductInsertTest_2', 'customfields') \
		.add_value('ProductInsertTest_textarea', 'ProductInsertTest_2', 'customfields') \
		.add_value('ProductInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductInsert)

	product = helper.get_product('ProductInsertTest_2')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductInsertTest_2'
	assert product.get_sku() == 'ProductInsertTest_2_Sku'
	assert product.get_name() == 'API Inserted Product 2'
	assert product.get_price() == 7.50
	assert product.get_cost() == 7.50
	assert product.get_id() > 0
	assert product.get_custom_field_values().has_value('ProductInsertTest_checkbox', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_checkbox', 'customfields') == '1'
	assert product.get_custom_field_values().has_value('ProductInsertTest_imageupload', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_imageupload', 'customfields') == 'graphics/00000001/ProductInsert.jpg'
	assert product.get_custom_field_values().has_value('ProductInsertTest_text', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_text', 'customfields') == 'ProductInsertTest_2'
	assert product.get_custom_field_values().has_value('ProductInsertTest_textarea', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_textarea', 'customfields') == 'ProductInsertTest_2'
	assert product.get_custom_field_values().has_value('ProductInsertTest_dropdown', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_dropdown', 'customfields') == 'Option2'


def product_insert_test_duplicate():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_Duplicate') \
		.set_product_sku('ProductInsertTest_Duplicate_Sku') \
		.set_product_name('API Inserted Product Duplicate') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductInsert)


def test_product_delete():
	"""
	Tests the Product_Delete API Call
	"""

	helper.provision_store('Product_Delete.xml')

	product_delete_test_deletion_by_id()
	product_delete_test_deletion_by_code()
	product_delete_test_deletion_by_sku()
	product_delete_test_deletion_by_edit_product()


def product_delete_test_deletion_by_id():
	product = helper.get_product('ProductDeleteTest_ID')

	assert isinstance(product, merchantapi.model.Product)

	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_id(product.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_ID')

	assert check is None


def product_delete_test_deletion_by_code():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_code('ProductDeleteTest_CODE')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_CODE')

	assert check is None


def product_delete_test_deletion_by_sku():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_sku('ProductDeleteTest_SKU')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_SKU')

	assert check is None


def product_delete_test_deletion_by_edit_product():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_edit_product('ProductDeleteTest_EDIT_PRODUCT')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_EDIT_PRODUCT')

	assert check is None


def test_product_update():
	"""
	Tests the Product_Update API Call
	"""

	helper.provision_store('Product_Update.xml')

	product_update_test_update()
	product_update_test_update_code()


def product_update_test_update():
	request = merchantapi.request.ProductUpdate(helper.init_client())

	request.set_edit_product('ProductUpdateTest_1') \
		.set_product_name('ProductUpdateTest_1 New Name') \
		.set_product_price(39.99) \
		.set_product_cost(29.99) \
		.set_product_active(True) \
		.set_product_taxable(True) \
		.set_product_sku('ProductUpdateTest_1_Changed_SKU') \
		.set_product_page_title('ProductUpdateTest_1 Changed Page Title')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductUpdate)

	product = helper.get_product('ProductUpdateTest_1')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_name() == 'ProductUpdateTest_1 New Name'
	assert product.get_price() == 39.99
	assert product.get_cost() == 29.99
	assert product.get_active() is True
	assert product.get_taxable() is True
	assert product.get_sku() == 'ProductUpdateTest_1_Changed_SKU'
	assert product.get_page_title() == 'ProductUpdateTest_1 Changed Page Title'


def product_update_test_update_code():
	request = merchantapi.request.ProductUpdate(helper.init_client())

	request.set_edit_product('ProductUpdateTest_3') \
		.set_product_code('ProductUpdateTest_3_Changed')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductUpdate)

	product = helper.get_product('ProductUpdateTest_3_Changed')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductUpdateTest_3_Changed'


def test_customer_address_list_load_query():
	"""
	Tests the CustomerAddressList_Load_Query API Call
	"""

	helper.provision_store('CustomerAddressList_Load_Query.xml')

	customer_address_list_load_query_test_list_load()
	customer_address_list_load_query_test_list_load_filtered()


def customer_address_list_load_query_test_list_load():
	customer = helper.get_customer('CustomerAddressListLoadQueryTest')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_login() == 'CustomerAddressListLoadQueryTest'
	assert customer.get_id() > 0

	request = merchantapi.request.CustomerAddressListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerAddressListLoadQueryTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListLoadQuery)

	assert isinstance(response.get_customer_addresses(), list)
	assert len(response.get_customer_addresses()) == 3

	for i, address in enumerate(response.get_customer_addresses()):
		assert isinstance(address, merchantapi.model.CustomerAddress)
		assert address.get_customer_id() == customer.get_id()


def customer_address_list_load_query_test_list_load_filtered():
	customer = helper.get_customer('CustomerAddressListLoadQueryTest')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_login() == 'CustomerAddressListLoadQueryTest'
	assert customer.get_id() > 0

	request = merchantapi.request.CustomerAddressListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerAddressListLoadQueryTest')
	request.set_filters(request.filter_expression().equal('fname', 'Joe'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListLoadQuery)

	assert isinstance(response.get_customer_addresses(), list)
	assert len(response.get_customer_addresses()) == 1

	for i, address in enumerate(response.get_customer_addresses()):
		assert isinstance(address, merchantapi.model.CustomerAddress)
		assert address.get_customer_id() == customer.get_id()
		assert address.get_first_name() == 'Joe'


def test_print_queue_list_load_query():
	"""
	Tests the PrintQueueList_Load_Query API Call
	"""

	print_queue_list_load_query_test_list_load()


def print_queue_list_load_query_test_list_load():
	request = merchantapi.request.PrintQueueListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueListLoadQuery)

	assert isinstance(response.get_print_queues(), list)

	for pq in response.get_print_queues():
		assert isinstance(pq, merchantapi.model.PrintQueue)


def test_print_queue_job_list_load_query():
	"""
	Tests the PrintQueueJobList_Load_Query API Call
	"""

	print_queue_job_list_load_query_test_list_load()
	print_queue_job_list_load_query_test_invalid_queue()


def print_queue_job_list_load_query_test_list_load():
	helper.create_print_queue('PrintQueueJobListLoadQueryTest')

	request = merchantapi.request.PrintQueueJobListLoadQuery(helper.init_client())

	request.set_edit_print_queue('PrintQueueJobListLoadQueryTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobListLoadQuery)

	assert isinstance(response.get_print_queue_jobs(), list)

	for pqj in response.get_print_queue_jobs():
		assert isinstance(pqj, merchantapi.model.PrintQueueJob)


def print_queue_job_list_load_query_test_invalid_queue():
	request = merchantapi.request.PrintQueueJobListLoadQuery(helper.init_client())

	request.set_edit_print_queue('InvalidPrintQueue')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PrintQueueJobListLoadQuery)


def test_print_queue_job_delete():
	"""
	Tests the PrintQueueJob_Delete API Call
	"""

	print_queue_job_delete_test_deletion()


def print_queue_job_delete_test_deletion():
	helper.create_print_queue('PrintQueueJobDeleteTest')

	insert_request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	insert_request.set_edit_print_queue('PrintQueueJobDeleteTest') \
		.set_print_queue_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	insert_response = insert_request.send()

	helper.validate_response_success(insert_response, merchantapi.response.PrintQueueJobInsert)

	assert insert_response.get_print_queue_job() is not None
	assert insert_response.get_print_queue_job().get_id() > 0

	request = merchantapi.request.PrintQueueJobDelete(helper.init_client())

	request.set_print_queue_job_id(insert_response.get_print_queue_job().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobDelete)


def test_print_queue_job_insert():
	"""
	Tests the PrintQueueJob_Insert API Call
	"""

	print_queue_job_insert_test_insertion()


def print_queue_job_insert_test_insertion():
	helper.create_print_queue('PrintQueueJobInsertTest')

	request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	request.set_edit_print_queue('PrintQueueJobInsertTest') \
		.set_print_queue_job_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobInsert)

	assert isinstance(response.get_print_queue_job(), merchantapi.model.PrintQueueJob)

	assert response.get_print_queue_job().get_id() > 0
	assert response.get_print_queue_job().get_description() == 'Description'
	assert response.get_print_queue_job().get_job_format() == 'Format'
	assert response.get_print_queue_job().get_job_data() == 'Data'


def test_print_queue_job_status():
	"""
	Tests the PrintQueueJob_Status API Call
	"""

	print_queue_job_status_test_get_status()


def print_queue_job_status_test_get_status():
	helper.create_print_queue('PrintQueueJobStatusTest')

	insert_request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	insert_request.set_edit_print_queue('PrintQueueJobStatusTest') \
		.set_print_queue_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	insert_response = insert_request.send()

	helper.validate_response_success(insert_response, merchantapi.response.PrintQueueJobInsert)

	assert insert_response.get_print_queue_job() is not None
	assert insert_response.get_print_queue_job().get_id() > 0

	request = merchantapi.request.PrintQueueJobStatus(helper.init_client())

	request.set_print_queue_job_id(insert_response.get_print_queue_job().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobStatus)

	assert response.get_status() not in (None, '')


def test_payment_method_list_load():
	"""
	Tests the PaymentMethodList_Load API Call
	"""

	helper.provision_store('PaymentMethodList_Load.xml')

	payment_method_list_load_test_list_load()


def payment_method_list_load_test_list_load():
	modules = helper.load_modules_by_feature('payment', ['cod', 'check'])

	assert isinstance(modules, list)
	assert len(modules) == 2

	request = merchantapi.request.PaymentMethodListLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PaymentMethodListLoad)

	assert isinstance(response.get_payment_methods(), list)
	assert len(response.get_payment_methods()) >= 2

	for pm in response.get_payment_methods():
		assert isinstance(pm, merchantapi.model.PaymentMethod)
		assert pm.get_module_api() > 0
		assert pm.get_module_id() > 0
		assert pm.get_method_code() not in (None, '')
		assert pm.get_method_name() not in (None, '')

	for module in modules:
		match = None

		for pm in response.get_payment_methods():
			if pm.get_module_id() == module['id']:
				match = pm

		assert match is not None


def test_order_create_from_order():
	"""
	Tests the Order_Create_FromOrder API Call
	"""

	helper.provision_store('Order_Create_FromOrder.xml')

	order_create_from_order_test_create()
	order_create_from_order_test_invalid_order()


def order_create_from_order_test_create():
	order = helper.get_order(10520)

	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() == 10520

	request = merchantapi.request.OrderCreateFromOrder(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreateFromOrder)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_id() != 10520


def order_create_from_order_test_invalid_order():
	request = merchantapi.request.OrderCreateFromOrder(helper.init_client())

	request.set_order_id(8980999)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderCreateFromOrder)


def test_customer_payment_card_list_load_query():
	"""
	Tests the CustomerPaymentCardList_Load_Query API Call
	"""

	helper.provision_store('MivaPay.xml')
	helper.provision_store('CustomerPaymentCardList_Load_Query.xml')

	customer_payment_card_list_load_query_test_list_load()


def customer_payment_card_list_load_query_test_list_load():
	cards = ['4788250000028291', '4055011111111111', '5454545454545454', '5405222222222226']
	lastfours = ['8291', '1111', '5454', '2226']

	mrequest = merchantapi.multicall.MultiCallRequest(helper.init_client())

	for card in cards:
		card_request = merchantapi.request.CustomerPaymentCardRegister(None)

		card_request.set_customer_login('CustomerPaymentCardList_Load_Query') \
			.set_first_name('John') \
			.set_last_name('Doe') \
			.set_card_type('MasterCard' if card[0] == 5 else 'Visa') \
			.set_card_number(card) \
			.set_expiration_month(8) \
			.set_expiration_year(2025) \
			.set_address1('1234 Test St') \
			.set_address2('Unit 123') \
			.set_city('San Diego') \
			.set_state('CA') \
			.set_zip('92009') \
			.set_country('USA')

		mrequest.add_request(card_request)

	mresponse = mrequest.send()

	helper.validate_response_success(mresponse, merchantapi.multicall.MultiCallResponse)

	assert isinstance(mresponse.get_responses(), list)

	for resp in mresponse.get_responses():
		helper.validate_response_success(resp, merchantapi.response.CustomerPaymentCardRegister)

	request = merchantapi.request.CustomerPaymentCardListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerPaymentCardList_Load_Query')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPaymentCardListLoadQuery)

	assert isinstance(response.get_customer_payment_cards(), list)
	assert len(response.get_customer_payment_cards()) == 4

	for card in response.get_customer_payment_cards():
		assert card.get_last_four() in lastfours


def test_category_product_list_load_query():
	"""
	Tests the CategoryProductList_Load_Query API Call
	"""

	helper.provision_store('CategoryProductList_Load_Query.xml')

	category_product_list_load_query_test_list_load()


def category_product_list_load_query_test_list_load():
	request = merchantapi.request.CategoryProductListLoadQuery(helper.init_client())

	request.set_edit_category('CategoryProductListLoadQueryTest_Category') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductListLoadQuery)

	assert isinstance(response.get_category_products(), list)
	assert len(response.get_category_products()) == 3

	for i, cp in enumerate(response.get_category_products()):
		assert isinstance(cp, merchantapi.model.CategoryProduct)
		assert cp.get_code() == 'CategoryProductListLoadQueryTest_Product_%d' % int(i+1)


def test_coupon_price_group_list_load_query():
	"""
	Tests the CouponPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('CouponPriceGroupList_Load_Query.xml')

	coupon_price_group_list_load_query_test_list_load()


def coupon_price_group_list_load_query_test_list_load():
	request = merchantapi.request.CouponPriceGroupListLoadQuery(helper.init_client())

	request.set_coupon_code('CouponPriceGroupListLoadQueryTest_Coupon') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupListLoadQuery)

	assert isinstance(response.get_coupon_price_groups(), list)
	assert len(response.get_coupon_price_groups()) == 3

	for i, cp in enumerate(response.get_coupon_price_groups()):
		assert isinstance(cp, merchantapi.model.CouponPriceGroup)
		assert cp.get_name() == 'CouponPriceGroupListLoadQueryTest_PriceGroup_%d' % int(i+1)


def test_price_group_product_list_load_query():
	"""
	Tests the PriceGroupProductList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupProductList_Load_Query.xml')

	price_group_product_list_load_query_test_list_load()


def price_group_product_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupProductListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupProductListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductListLoadQuery)

	assert isinstance(response.get_price_group_products(), list)
	assert len(response.get_price_group_products()) == 5

	for i, pgp in enumerate(response.get_price_group_products()):
		assert isinstance(pgp, merchantapi.model.PriceGroupProduct)
		assert pgp.get_code() == 'PriceGroupProductListLoadQueryTest_0%d' % int(i+1)
		assert pgp.get_name() == 'PriceGroupProductListLoadQueryTest_0%d' % int(i+1)


def test_customer_price_group_list_load_query():
	"""
	Tests the CustomerPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('CustomerPriceGroupList_Load_Query.xml')

	customer_price_group_list_load_query_test_list_load()


def customer_price_group_list_load_query_test_list_load():
	request = merchantapi.request.CustomerPriceGroupListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerPriceGroupListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPriceGroupListLoadQuery)

	assert isinstance(response.get_customer_price_groups(), list)
	assert len(response.get_customer_price_groups()) == 3

	for i, customerpricegroup in enumerate(response.get_customer_price_groups()):
		assert isinstance(customerpricegroup, merchantapi.model.CustomerPriceGroup)
		assert customerpricegroup.get_name() == 'CustomerPriceGroupListLoadQueryTest_%d' % int(i+1)
		assert customerpricegroup.get_description() == 'CustomerPriceGroupListLoadQueryTest_%d' % int(i+1)
		assert customerpricegroup.get_customer_scope() == merchantapi.model.CustomerPriceGroup.ELIGIBILITY_CUSTOMER
		assert customerpricegroup.get_module().get_code() == 'discount_product'


def test_price_group_customer_list_load_query():
	"""
	Tests the PriceGroupCustomerList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupCustomerList_Load_Query.xml')

	price_group_customer_list_load_query_test_list_load()


def price_group_customer_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupCustomerListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupCustomerListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCustomerListLoadQuery)

	assert isinstance(response.get_price_group_customers(), list)
	assert len(response.get_price_group_customers()) == 5

	for i, pgc in enumerate(response.get_price_group_customers()):
		assert isinstance(pgc, merchantapi.model.PriceGroupCustomer)
		assert pgc.get_login() == 'PriceGroupCustomerListLoadQueryTest_0%d' % int(i+1)
		assert pgc.get_business_title() == 'PriceGroupCustomerListLoadQueryTest'
		assert pgc.get_assigned() is True


def test_branch_copy():
	"""
	Tests the Branch_Copy API Call
	"""

	branch_copy_test_copy()


def branch_copy_test_copy():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	request = merchantapi.request.BranchCopy(helper.init_client(), default_branch)

	request.set_destination_branch_id(create_response.get_branch().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchCopy)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)

	assert response.get_changeset().get_id() > 0
	assert response.get_changeset().get_branch_id() > 0


def test_branch_create():
	"""
	Tests the Branch_Create API Call
	"""

	branch_create_test_create()


def branch_create_test_create():
	helper.delete_branch('Production Copy')

	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.BranchCreate(helper.init_client(), branch)

	request.set_name('Production Copy')
	request.set_color('#000000')

	assert branch.get_id() == request.get_parent_branch_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchCreate)

	assert isinstance(response.get_branch(), merchantapi.model.Branch)


def test_branch_delete():
	"""
	Tests the Branch_Delete API Call
	"""

	branch_delete_test_deletion()


def branch_delete_test_deletion():
	branch = helper.get_branch('Production Copy')

	if branch is None:
		copybranch = helper.get_branch('Production')
		assert isinstance(copybranch, merchantapi.model.Branch)
		copyrequest = merchantapi.request.BranchCreate(helper.init_client(), copybranch)
		copyrequest.set_name('Production Copy')
		copyrequest.set_color('#000000')

		copyresponse = copyrequest.send()
		helper.validate_response_success(copyresponse, merchantapi.response.BranchCreate)

		branch = copyresponse.get_branch()

	request = merchantapi.request.BranchDelete(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchDelete)


def test_changeset_create():
	"""
	Tests the Changeset_Create API Call
	"""

	changeset_create_test_creation()


def changeset_create_test_creation():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	assert request.get_branch_id() == branch.get_id()

	# Load a Changeset
	load_changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	load_changeset_response = load_changeset_request.send()

	helper.validate_response_success(load_changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert isinstance(load_changeset_response.get_changesets(), list)
	assert len(load_changeset_response.get_changesets()) > 0

	changeset = load_changeset_response.get_changesets()[0]

	assert isinstance(changeset, merchantapi.model.Changeset)

	# Load a Template
	load_template_request = merchantapi.request.BranchTemplateVersionListLoadQuery(helper.init_client(), branch)

	load_template_request.set_filters(load_template_request.filter_expression().equal('filename', 'sfnt.mvc'))
	load_template_request.set_on_demand_columns(load_template_request.get_available_on_demand_columns())
	load_template_request.set_changeset_id(changeset.get_id())

	load_template_response = load_template_request.send()

	helper.validate_response_success(load_template_response, merchantapi.response.BranchTemplateVersionListLoadQuery)

	assert isinstance(load_template_response.get_branch_template_versions(), list)
	assert len(load_template_response.get_branch_template_versions()) > 0

	version = load_template_response.get_branch_template_versions()[0]

	assert isinstance(version, merchantapi.model.BranchTemplateVersion)

	# Add a Change
	change1 = merchantapi.model.TemplateChange()

	source = version.get_source()

	assert isinstance(source, str)
	assert len(source) > 0

	if '<body class="SFNT">HELLO_WORLD' in source:
		change1.set_template_filename('sfnt.mvc').set_source(source.replace('<body class="SFNT">HELLO_WORLD', '<body class="SFNT">'))
	else:
		change1.set_template_filename('sfnt.mvc').set_source(source.replace('<body class="SFNT">', '<body class="SFNT">HELLO_WORLD'))

	request.add_template_change(change1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCreate)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)


def test_branch_list_load_query():
	"""
	Tests the BranchList_Load_Query API Call
	"""

	branch_list_load_query_test_list_load()


def branch_list_load_query_test_list_load():
	request = merchantapi.request.BranchListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchListLoadQuery)

	assert len(response.get_branches()) > 0

	for e in response.get_branches():
		assert isinstance(e, merchantapi.model.Branch)



def test_branch_list_delete():
	"""
	Tests the BranchList_Delete API Call
	"""

	branch_list_delete_test()


def branch_list_delete_test():
	helper.delete_branch('Production Copy')
	helper.delete_branch('Production Copy 1')
	helper.delete_branch('Production Copy 2')

	production_branch = helper.get_branch('Production')

	branch1 = helper.create_branch('Production Copy', '#000000', production_branch)
	branch2 = helper.create_branch('Production Copy 1', '#000000', production_branch)
	branch3 = helper.create_branch('Production Copy 2', '#000000', production_branch)

	request = merchantapi.request.BranchListDelete(helper.init_client())

	request.add_branch(branch1)
	request.add_branch(branch2)
	request.add_branch(branch3)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchListDelete)

	assert response.get_processed() == 3


def test_branch_template_version_list_load_query():
	"""
	Tests the BranchTemplateVersionList_Load_Query API Call
	"""

	branch_template_version_list_load_query_test_list_load()


def branch_template_version_list_load_query_test_list_load():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.BranchTemplateVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchTemplateVersionListLoadQuery)

	assert len(response.get_branch_template_versions()) > 0

	for e in response.get_branch_template_versions():
		assert isinstance(e, merchantapi.model.BranchTemplateVersion)


def test_changeset_template_version_list_load_query():
	"""
	Tests the ChangesetTemplateVersionList_Load_Query API Call
	"""

	changeset_template_version_list_load_query_test_list_load()


def changeset_template_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None
	
	# Load a Changeset
	load_changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	load_changeset_response = load_changeset_request.send()

	helper.validate_response_success(load_changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert isinstance(load_changeset_response.get_changesets(), list)
	assert len(load_changeset_response.get_changesets()) > 0

	changeset = load_changeset_response.get_changesets()[0]

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetTemplateVersionListLoadQuery(helper.init_client(), changeset)
	
	assert changeset.get_id() == request.get_changeset_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetTemplateVersionListLoadQuery)

	assert len(response.get_changeset_template_versions()) > 0

	for e in response.get_changeset_template_versions():
		assert isinstance(e, merchantapi.model.ChangesetTemplateVersion)


def test_changeset_list_load_query():
	"""
	Tests the ChangesetTemplateVersionList_Load_Query API Call
	"""

	changeset_list_load_query_test_list_load()


def changeset_list_load_query_test_list_load():
	request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())

	request.set_branch_name('Production')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetListLoadQuery)

	assert len(response.get_changesets()) > 0

	for e in response.get_changesets():
		assert isinstance(e, merchantapi.model.Changeset)


def test_changeset_list_merge():
	"""
	Tests the ChangesetList_Merge API Call
	"""

	changeset_list_merge_test_merge()


def changeset_list_merge_test_merge():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create 3 seperate Changes

	create_changeset_request1 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)
	create_changeset_request2 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)
	create_changeset_request3 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	template1 = helper.get_branch_template_version('sfnt.mvc', branch)
	template2 = helper.get_branch_template_version('prod.mvc', branch)
	template3 = helper.get_branch_template_version('ctgy.mvc', branch)

	change1 = merchantapi.model.TemplateChange()
	change2 = merchantapi.model.TemplateChange()
	change3 = merchantapi.model.TemplateChange()

	change1.set_template_filename('sfnt.mvc').set_source(template1.get_source().replace('<body class="SFNT">', '<body class="SFNT">HELLO_WORLD'))
	change2.set_template_filename('prod.mvc').set_source(template2.get_source().replace('<body class="PROD">', '<body class="PROD">HELLO_WORLD'))
	change3.set_template_filename('ctgy.mvc').set_source(template3.get_source().replace('<body class="CTGY">', '<body class="CTGY">HELLO_WORLD'))

	create_changeset_request1.add_template_change(change1)
	create_changeset_request2.add_template_change(change2)
	create_changeset_request3.add_template_change(change3)

	create_changeset_response1 = create_changeset_request1.send()
	create_changeset_response2 = create_changeset_request2.send()
	create_changeset_response3 = create_changeset_request3.send()

	helper.validate_response_success(create_changeset_response1, merchantapi.response.ChangesetCreate)
	helper.validate_response_success(create_changeset_response2, merchantapi.response.ChangesetCreate)
	helper.validate_response_success(create_changeset_response3, merchantapi.response.ChangesetCreate)

	assert isinstance(create_changeset_response1.get_changeset(), merchantapi.model.Changeset)
	assert isinstance(create_changeset_response2.get_changeset(), merchantapi.model.Changeset)
	assert isinstance(create_changeset_response3.get_changeset(), merchantapi.model.Changeset)

	# Now merge the changes into one change

	request = merchantapi.request.ChangesetListMerge(helper.init_client(), branch)

	request.add_changeset(create_changeset_response1.get_changeset())
	request.add_changeset(create_changeset_response2.get_changeset())
	request.add_changeset(create_changeset_response3.get_changeset())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetListMerge)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)


def test_changeset_change_list_load_query():
	"""
	Tests the ChangesetChangeList_Load_Query API Call
	"""

	changeset_change_list_load_query_test_list_load()


def changeset_change_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create 3 Changes in one changeset

	create_changeset_request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	template1 = helper.get_branch_template_version('sfnt.mvc', branch)
	template2 = helper.get_branch_template_version('prod.mvc', branch)
	template3 = helper.get_branch_template_version('ctgy.mvc', branch)

	change1 = merchantapi.model.TemplateChange()
	change2 = merchantapi.model.TemplateChange()
	change3 = merchantapi.model.TemplateChange()

	change1.set_template_filename('sfnt.mvc').set_source(template1.get_source().replace('<body class="SFNT">', '<body class="SFNT">HELLO_WORLD'))
	change2.set_template_filename('prod.mvc').set_source(template2.get_source().replace('<body class="PROD">', '<body class="PROD">HELLO_WORLD'))
	change3.set_template_filename('ctgy.mvc').set_source(template3.get_source().replace('<body class="CTGY">', '<body class="CTGY">HELLO_WORLD'))

	create_changeset_request.add_template_change(change1)
	create_changeset_request.add_template_change(change2)
	create_changeset_request.add_template_change(change3)

	create_changeset_response = create_changeset_request.send()

	helper.validate_response_success(create_changeset_response, merchantapi.response.ChangesetCreate)

	changeset = create_changeset_response.get_changeset()

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetChangeListLoadQuery(helper.init_client(), changeset)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetChangeListLoadQuery)

	assert len(response.get_changeset_changes()) == 3

	for change in response.get_changeset_changes():
		assert isinstance(change, merchantapi.model.ChangesetChange)


def test_branch_css_resource_version_list_load_query():
	"""
	Tests the BranchCSSResourceVersionList_Load_Query API Call
	"""

	branch_css_resource_version_list_load_query_test_list_load()


def branch_css_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	request = merchantapi.request.BranchCSSResourceVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchCSSResourceVersionListLoadQuery)

	assert len(response.get_branch_css_resource_versions()) > 0

	for version in response.get_branch_css_resource_versions():
		assert isinstance(version, merchantapi.model.CSSResourceVersion)


def test_branch_java_script_resource_version_list_load_query():
	"""
	Tests the BranchJavaScriptResourceVersionList_Load_Query API Call
	"""

	branch_java_script_resource_version_list_load_query_test_list_load()


def branch_java_script_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchJavaScriptResourceVersionListLoadQuery)

	assert len(response.get_branch_java_script_resource_versions()) > 0

	for version in response.get_branch_java_script_resource_versions():
		assert isinstance(version, merchantapi.model.JavaScriptResourceVersion)


def test_changeset_css_resource_version_list_load_query():
	"""
	Tests the ChangesetCSSResourceVersionList_Load_Query API Call
	"""

	helper.provision_store('ChangesetCSSResourceVersionList_Load_Query.xml')

	changeset_css_resource_version_list_load_query_test_list_load()


def changeset_css_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(branch.get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetCSSResourceVersionListLoadQuery(helper.init_client())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ChangesetCSSResourceVersionListLoadQuery%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCSSResourceVersionListLoadQuery)

	assert len(response.get_changeset_css_resource_versions()) == 6

	for version in response.get_changeset_css_resource_versions():
		assert isinstance(version, merchantapi.model.CSSResourceVersion)

		assert len(version.get_attributes()) > 0

		for attribute in version.get_attributes():
			assert isinstance(attribute, merchantapi.model.CSSResourceVersionAttribute)


def test_changeset_java_script_resource_version_list_load_query():
	"""
	Tests the ChangesetJavaScriptResourceVersionList_Load_Query API Call
	"""

	helper.provision_store('ChangesetJavaScriptResourceVersionList_Load_Query.xml')

	changeset_java_script_resource_version_list_load_query_test_list_load()


def changeset_java_script_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(create_response.get_branch().get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetJavaScriptResourceVersionListLoadQuery(helper.init_client())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ChangesetJavaScriptResourceVersionListLoadQuery%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetJavaScriptResourceVersionListLoadQuery)

	assert len(response.get_changeset_java_script_resource_versions()) == 6

	for version in response.get_changeset_java_script_resource_versions():
		assert isinstance(version, merchantapi.model.ChangesetJavaScriptResourceVersion)

		assert len(version.get_attributes()) > 0

		for attribute in version.get_attributes():
			assert isinstance(attribute, merchantapi.model.JavaScriptResourceVersionAttribute)


def test_branch_property_version_list_load_query():
	"""
	Tests the BranchPropertyVersionList_Load_Query API Call
	"""

	branch_property_version_list_load_query_test_list_load()


def branch_property_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	request = merchantapi.request.BranchPropertyVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchPropertyVersionListLoadQuery)

	assert len(response.get_branch_property_versions()) > 0

	for v in response.get_branch_property_versions():
		assert isinstance(v, merchantapi.model.BranchPropertyVersion)


def test_changeset_property_version_list_load_query():
	"""
	Tests the ChangesetPropertyVersionList_Load_Query API Call
	"""

	changeset_property_version_list_load_query_test_list_load()


def changeset_property_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetPropertyVersionListLoadQuery(helper.init_client(), changeset_response.get_changesets()[0])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetPropertyVersionListLoadQuery)

	assert len(response.get_changeset_property_versions()) > 0

	for v in response.get_changeset_property_versions():
		assert isinstance(v, merchantapi.model.ChangesetPropertyVersion)


def test_order_price_group_update_assigned():
	"""
	Tests the OrderPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('OrderPriceGroup_Update_Assigned.xml')

	order_price_group_update_assigned_test_assignment()
	order_price_group_update_assigned_test_unassignment()


def order_price_group_update_assigned_test_assignment():
	order = helper.get_order(3651499)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_price_group_name('OrderPriceGroup_Update_Assigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupUpdateAssigned)

	check_request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)
	check_request.set_filters(
		check_request.filter_expression()
		.equal('name', 'OrderPriceGroup_Update_Assigned_1')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(True)
	check_request.set_unassigned(False)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(check_response.get_order_price_groups()) == 1
	assert check_response.get_order_price_groups()[0].get_name() == 'OrderPriceGroup_Update_Assigned_1'


def order_price_group_update_assigned_test_unassignment():
	order = helper.get_order(3651499)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_price_group_name('OrderPriceGroup_Update_Assigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupUpdateAssigned)

	check_request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)

	check_request.set_filters(
		check_request.filter_expression()
		.equal('name', 'OrderPriceGroup_Update_Assigned_2')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(check_response.get_order_price_groups()) == 1
	assert check_response.get_order_price_groups()[0].get_name() == 'OrderPriceGroup_Update_Assigned_2'


def test_order_price_group_list_load_query():
	"""
	Tests the OrderPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('OrderPriceGroupList_Load_Query.xml')

	order_price_group_list_load_query_test_list_load()


def order_price_group_list_load_query_test_list_load():
	order = helper.get_order(3651498)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert order.get_id() == request.get_order_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(response.get_order_price_groups()) == 2
	for order_price_group in response.get_order_price_groups():
		assert isinstance(order_price_group, merchantapi.model.OrderPriceGroup)
		assert order_price_group.get_name() in ('OrderPriceGroupListLoadQuery_1', 'OrderPriceGroupListLoadQuery_2')


def test_order_coupon_update_assigned():
	"""
	Tests the OrderPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('OrderCoupon_Update_Assigned.xml')

	order_coupon_update_assigned_test_assignment()
	order_coupon_update_assigned_test_unassignment()


def order_coupon_update_assigned_test_assignment():
	order = helper.get_order(3651500)

	assert order is not None

	request = merchantapi.request.OrderCouponUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_coupon_code('OrderCouponUpdateAssigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponUpdateAssigned)

	check_request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(True)
	check_request.set_unassigned(False)
	check_request.set_filters(
		check_request.filter_expression()
		.equal('code', 'OrderCouponUpdateAssigned_1')
	)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(check_response.get_order_coupons()) == 1
	assert check_response.get_order_coupons()[0].get_code() == 'OrderCouponUpdateAssigned_1'


def order_coupon_update_assigned_test_unassignment():
	order = helper.get_order(3651500)

	assert order is not None

	request = merchantapi.request.OrderCouponUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_coupon_code('OrderCouponUpdateAssigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponUpdateAssigned)

	check_request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	check_request.set_filters(
		check_request.filter_expression()
		.equal('code', 'OrderCouponUpdateAssigned_2')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(check_response.get_order_coupons()) == 1
	assert check_response.get_order_coupons()[0].get_code() == 'OrderCouponUpdateAssigned_2'


def test_order_coupon_list_load_query():
	"""
	Tests the OrderCouponList_Load_Query API Call
	"""

	helper.provision_store('OrderCouponList_Load_Query.xml')

	order_coupon_list_load_query_test_list_load()


def order_coupon_list_load_query_test_list_load():
	order = helper.get_order(3651501)

	assert order is not None

	request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert order.get_id() == request.get_order_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(response.get_order_coupons()) == 3
	for order_coupon in response.get_order_coupons():
		assert isinstance(order_coupon, merchantapi.model.OrderCoupon)
		assert order_coupon.get_code() in ('OrderCouponList_Load_Query_1', 'OrderCouponList_Load_Query_2', 'OrderCouponList_Load_Query_3')


def test_customer_history_list_load_query():
	"""
	Tests the CustomerCreditHistoryList_Load_Query API Call
	"""

	helper.provision_store('CustomerCreditHistoryList_Load_Query.xml')

	customer_history_list_load_query_test_list_load()


def customer_history_list_load_query_test_list_load():
	customer = helper.get_customer('CustomerHistoryListLoadQuery')

	assert customer is not None

	for i in range(0, 3):
		insert_request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)
		insert_request.set_amount(1.99)
		insert_request.set_description('DESCRIPTION')
		insert_request.set_transaction_reference('REFERENCE')
		helper.validate_response_success(insert_request.send(), merchantapi.response.CustomerCreditHistoryInsert)

	request = merchantapi.request.CustomerCreditHistoryListLoadQuery(helper.init_client(), customer)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryListLoadQuery)

	assert len(response.get_customer_credit_history()) == 3
	for history in response.get_customer_credit_history():
		assert isinstance(history, merchantapi.model.CustomerCreditHistory)
		assert history.get_description() == 'DESCRIPTION'
		assert history.get_transaction_reference() == 'REFERENCE'
		assert history.get_amount() == 1.99


def test_customer_history_insert():
	"""
	Tests the CustomerCreditHistory_Insert API Call
	"""

	helper.provision_store('CustomerCreditHistory_Insert.xml')

	customer_history_insert_test_insertion()


def customer_history_insert_test_insertion():
	customer = helper.get_customer('CustomerCreditHistoryInsert')

	assert customer is not None

	request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)

	assert request.get_customer_id() == customer.get_id()

	request.set_amount(1.99)
	request.set_description('DESCRIPTION')
	request.set_transaction_reference('REFERENCE')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryInsert)


def test_customer_history_delete():
	"""
	Tests the CustomerCreditHistory_Delete API Call
	"""

	helper.provision_store('CustomerCreditHistory_Delete.xml')

	customer_history_delete_test_deletion()


def customer_history_delete_test_deletion():
	customer = helper.get_customer('CustomerCreditHistoryDelete')

	assert customer is not None

	add_request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)

	assert add_request.get_customer_id() == customer.get_id()

	add_request.set_amount(1.99)
	add_request.set_description('DESCRIPTION')
	add_request.set_transaction_reference('REFERENCE')

	add_response = add_request.send()

	helper.validate_response_success(add_response, merchantapi.response.CustomerCreditHistoryInsert)

	load_request = merchantapi.request.CustomerCreditHistoryListLoadQuery(helper.init_client(), customer)

	load_response = load_request.send()

	helper.validate_response_success(load_response, merchantapi.response.CustomerCreditHistoryListLoadQuery)

	assert len(load_response.get_customer_credit_history()) == 1

	history = load_response.get_customer_credit_history()[0]

	assert isinstance(history, merchantapi.model.CustomerCreditHistory)

	request = merchantapi.request.CustomerCreditHistoryDelete(helper.init_client(), history)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryDelete)


def test_order_item_list_create_return():
	"""
	Tests the OrderItemList_CreateReturn API Call
	"""

	helper.provision_store('OrderItemList_CreateReturn.xml')

	order_item_list_create_return_create_return()
	order_item_list_create_return_invalid_order()
	order_item_list_create_return_invalid_line_ids()


def order_item_list_create_return_create_return():
	order = helper.get_order(529555)

	assert order is not None

	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	for item in order.get_items():
		request.add_order_item(item)

	assert len(request.get_line_ids()) == len(order.get_items())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCreateReturn)

	assert isinstance(response.get_order_return(), merchantapi.model.OrderReturn)
	assert response.get_order_return().get_status() == merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_ISSUED


def order_item_list_create_return_invalid_order():
	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client())
	request.set_order_id(999999999)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemListCreateReturn)


def order_item_list_create_return_invalid_line_ids():
	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client())
	request.set_order_id(529555)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemListCreateReturn)


def test_order_return_list_received():
	"""
	Tests the OrderReturnList_Received API Call
	"""

	helper.provision_store('OrderReturnList_Received.xml')

	order_return_list_received_test_received_return()


def order_return_list_received_test_received_return():
	order = helper.get_order(529556)

	assert order is not None

	create_request = merchantapi.request.OrderItemListCreateReturn(helper.init_client(), order)

	assert create_request.get_order_id() == order.get_id()

	for item in order.get_items():
		create_request.add_order_item(item)

	assert len(create_request.get_line_ids()) == len(order.get_items())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.OrderItemListCreateReturn)

	assert isinstance(create_response.get_order_return(), merchantapi.model.OrderReturn)
	assert create_response.get_order_return().get_status() == merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_ISSUED

	request = merchantapi.request.OrderReturnListReceived(helper.init_client())

	for item in order.get_items():
		received_return = merchantapi.model.ReceivedReturn()
		received_return.set_return_id(create_response.get_order_return().get_id())
		received_return.set_adjust_inventory(1)

		request.add_received_return(received_return)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderReturnListReceived)

	check_order = helper.get_order(order.get_id())

	assert check_order is not None

	for item in check_order.get_items():
		assert item.get_status() ==  merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_RECEIVED


def test_version_settings():
	"""
	Tests the VersionSettings model within various API Calls
	"""

	version_settings_test_serialization()
	version_settings_test_deserialization()


def version_settings_test_serialization():
	data = {
		"foo": {
			"bar": "bin",
			"baz": 1,
			"bin": 1.99
		},
		"bar": {
			"array": [
				"foo",
				"bar"
			]
		},
		"baz": "bar"
	}

	model = merchantapi.model.VersionSettings(data)

	serialized = model.to_dict()

	assert isinstance(serialized, dict)

	assert 'foo' in serialized
	assert 'bar' in serialized
	assert 'baz' in serialized

	assert serialized['foo']['bar'] == 'bin'
	assert serialized['foo']['baz'] == 1
	assert serialized['foo']['bin'] == 1.99
	assert serialized['bar']['array'][0] == 'foo'
	assert serialized['bar']['array'][1] == 'bar'
	assert serialized['baz'] == 'bar'


def version_settings_test_deserialization():
	data = {
		"foo": {
			"bar": "bin",
			"baz": 1,
			"bin": 1.99
		},
		"bar": {
			"array": [
				"foo",
				"bar"
			]
		},
		"baz": "bar"
	}

	model = merchantapi.model.VersionSettings(data)

	assert model.is_dict() is True
	assert model.is_scalar() is False
	assert model.is_list() is False

	assert model.has_item('foo') is True
	assert model.item_has_property('foo', 'bar') is True
	assert model.item_has_property('foo', 'baz') is True
	assert model.item_has_property('foo', 'bin') is True
	assert model.get_item_property('foo', 'bar') == "bin"
	assert model.get_item_property('foo', 'baz') == 1
	assert model.get_item_property('foo', 'bin') == 1.99

	assert model.has_item('bar') is True
	assert model.item_has_property('bar', 'array') is True
	assert isinstance(model.get_item_property('bar', 'array'), list)

	assert model.has_item('baz') is True
	assert model.item_has_property('baz', 'NONE') is False
	assert model.get_item('baz') == 'bar'


def test_resource_group_list_load_query():
	"""
	Tests the ResourceGroupList_Load_Query  API Call
	"""

	resource_group_list_load_query_test_list_load()


def resource_group_list_load_query_test_list_load():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(create_response.get_branch().get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ResourceGroupListLoadQuery(helper.init_client(), create_response.get_branch())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ResourceGroupListLoadQuery)


def test_miva_merchant_version():
	"""
	Tests the MivaMerchantVersion API Call
	"""

	request = merchantapi.request.MivaMerchantVersion(helper.init_client())
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.MivaMerchantVersion)

	assert isinstance(response.get_merchant_version(), merchantapi.model.MerchantVersion)

	assert isinstance(response.get_merchant_version().get_version(), str) and len(response.get_merchant_version().get_version())
	assert isinstance(response.get_merchant_version().get_major(), int) and response.get_merchant_version().get_major() >= 10
	assert isinstance(response.get_merchant_version().get_minor(), int) and response.get_merchant_version().get_minor() >= 0
	assert isinstance(response.get_merchant_version().get_bugfix(), int) and response.get_merchant_version().get_bugfix() >= 0


def test_attribute_template_list_load_query():
	"""
	Tests the AttributeTemplateList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateList_Load_Query.xml')

	attribute_template_list_load_query_test_list_load()


def attribute_template_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'ATLLQ%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateListLoadQuery)

	assert len(response.get_attribute_templates()) > 0

	for a in response.get_attribute_templates():
		assert 'ATLLQ' in a.get_code()


def test_attribute_template_attribute_list_load_query():
	"""
	Tests the AttributeTemplateAttributeList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateAttributeList_Load_Query.xml')

	attribute_template_attribute_list_load_query_test_list_load()


def attribute_template_attribute_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateAttributeListLoadQuery(helper.init_client())

	request.set_attribute_template_code('ATALLQ_Template_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeListLoadQuery)

	assert len(response.get_attribute_template_attributes()) > 0

	for a in response.get_attribute_template_attributes():
		assert 'ATALLQ' in a.get_code()


def test_attribute_template_option_list_load_attribute():
	"""
	Tests the AttributeTemplateOptionList_Load_Attribute API Call
	"""

	helper.provision_store('AttributeTemplateOptionList_Load_Attribute.xml')

	attribute_template_option_list_load_attribute_test_list_load()


def attribute_template_option_list_load_attribute_test_list_load():
	request = merchantapi.request.AttributeTemplateOptionListLoadAttribute(helper.init_client())

	request.set_attribute_template_code('ATALLQ_Template_1')
	request.set_attribute_template_attribute_code('ATALLQ_Attribute_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionListLoadAttribute)

	assert len(response.get_attribute_template_options()) == 3

	for o in response.get_attribute_template_options():
		assert 'ATALLQ_Option_' in o.get_code()


def test_attribute_template_attribute_delete():
	"""
	Tests the AttributeTemplateAttribute_Delete API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Delete.xml')

	attribute_template_attribute_delete_test_deletion()


def attribute_template_attribute_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateAttributeDelete(helper.init_client())

	request.set_attribute_template_code('ATAD_Template_1')
	request.set_attribute_template_attribute_code('ATAD_Attribute_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeDelete)

	check = helper.get_attribute_template_attribute('ATAD_Template_1', 'ATAD_Attribute_1')
	assert check is None


def test_attribute_template_attribute_insert():
	"""
	Tests the AttributeTemplateAttribute_Insert API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Insert.xml')

	attribute_template_attribute_insert_test_insertion()


def attribute_template_attribute_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateAttributeInsert(helper.init_client())

	request.set_attribute_template_code('ATAI_Template_1')
	request.set_code('ATAI_Attribute_1')
	request.set_prompt('ATAI_Attribute_1')
	request.set_price(1.11)
	request.set_cost(2.22)
	request.set_weight(3.33)
	request.set_type('checkbox')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeInsert)

	assert isinstance(response.get_attribute_template_attribute(), merchantapi.model.AttributeTemplateAttribute)
	assert response.get_attribute_template_attribute().get_attribute_template_id() > 0
	assert response.get_attribute_template_attribute().get_code() == 'ATAI_Attribute_1'
	assert response.get_attribute_template_attribute().get_prompt() == 'ATAI_Attribute_1'
	assert response.get_attribute_template_attribute().get_type() == 'checkbox'
	assert response.get_attribute_template_attribute().get_price() == 1.11
	assert response.get_attribute_template_attribute().get_cost() == 2.22
	assert response.get_attribute_template_attribute().get_weight() == 3.33

	check = helper.get_attribute_template_attribute('ATAI_Template_1', 'ATAI_Attribute_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_attribute().get_id()


def test_attribute_template_attribute_update():
	"""
	Tests the AttributeTemplateAttribute_Update API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Update.xml')

	attribute_template_attribute_update_test_update()


def attribute_template_attribute_update_test_update():
	attribute = helper.get_attribute_template_attribute('ATAU_Template_1', 'ATAU_Attribute_1')

	assert attribute is not None

	request = merchantapi.request.AttributeTemplateAttributeUpdate(helper.init_client())

	request.set_attribute_template_code('ATAU_Template_1')
	request.set_attribute_template_attribute_code('ATAU_Attribute_1')
	request.set_code('ATAU_Attribute_1_Updated')
	request.set_prompt('ATAU_Attribute_1_Updated')
	request.set_price(1.12)
	request.set_cost(2.23)
	request.set_weight(3.34)
	request.set_type('checkbox')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeUpdate)

	check = helper.get_attribute_template_attribute('ATAU_Template_1', 'ATAU_Attribute_1_Updated')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_attribute_template_id() > 0
	assert check.get_code() == 'ATAU_Attribute_1_Updated'
	assert check.get_prompt() == 'ATAU_Attribute_1_Updated'
	assert check.get_type() == 'checkbox'
	assert check.get_price() == 1.12
	assert check.get_cost() == 2.23
	assert check.get_weight() == 3.34


def test_attribute_template_option_delete():
	"""
	Tests the AttributeTemplateOption_Delete API Call
	"""

	helper.provision_store('AttributeTemplateOption_Delete.xml')

	attribute_template_option_delete_test_deletion()


def attribute_template_option_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateOptionDelete(helper.init_client())

	request.set_attribute_template_code('ATOD_Template_1')
	request.set_attribute_template_attribute_code('ATOD_Attribute_1')
	request.set_attribute_template_option_code('ATOD_Option_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionDelete)

	check = helper.get_attribute_template_option('ATOD_Template_1', 'ATOD_Attribute_1', 'ATOD_Option_1')

	assert check is None


def test_attribute_template_option_insert():
	"""
	Tests the AttributeTemplateOption_Insert API Call
	"""

	helper.provision_store('AttributeTemplateOption_Insert.xml')

	attribute_template_option_insert_test_insertion()


def attribute_template_option_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateOptionInsert(helper.init_client())

	request.set_attribute_template_code('ATOI_Template_1')
	request.set_attribute_template_attribute_code('ATOI_Attribute_1')
	request.set_code('ATOI_Option_1')
	request.set_prompt('ATOI_Option_1')
	request.set_price(2.22)
	request.set_cost(3.33)
	request.set_weight(4.44)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionInsert)

	assert isinstance(response.get_attribute_template_option(), merchantapi.model.AttributeTemplateOption)
	assert response.get_attribute_template_option().get_code() == 'ATOI_Option_1'
	assert response.get_attribute_template_option().get_prompt() == 'ATOI_Option_1'
	assert response.get_attribute_template_option().get_price() == 2.22
	assert response.get_attribute_template_option().get_cost() == 3.33
	assert response.get_attribute_template_option().get_weight() == 4.44

	check = helper.get_attribute_template_option('ATOI_Template_1', 'ATOI_Attribute_1', 'ATOI_Option_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_option().get_id()


def test_attribute_template_option_update():
	"""
	Tests the AttributeTemplateOption_Update API Call
	"""

	helper.provision_store('AttributeTemplateOption_Update.xml')

	attribute_template_option_update_test_update()


def attribute_template_option_update_test_update():
	request = merchantapi.request.AttributeTemplateOptionUpdate(helper.init_client())

	request.set_attribute_template_code('ATOU_Template_1')
	request.set_attribute_template_attribute_code('ATOU_Attribute_1')
	request.set_attribute_template_option_code('ATOU_Option_1')
	request.set_code('ATOU_Option_1_Updated')
	request.set_prompt('ATOU_Option_1_Updated')
	request.set_price(1.13)
	request.set_cost(2.23)
	request.set_weight(3.34)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionUpdate)

	check = helper.get_attribute_template_option('ATOU_Template_1', 'ATOU_Attribute_1', 'ATOU_Option_1_Updated')

	assert check is not None
	assert check.get_code() == 'ATOU_Option_1_Updated'
	assert check.get_prompt() == 'ATOU_Option_1_Updated'
	assert check.get_price() == 1.13
	assert check.get_cost() == 2.23
	assert check.get_weight() == 3.34


def test_attribute_template_insert():
	"""
	Tests the AttributeTemplate_Insert API Call
	"""

	helper.provision_store('AttributeTemplate_Insert.xml')

	attribute_template_insert_test_insertion()


def attribute_template_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateInsert(helper.init_client())

	request.set_code('AttributeTemplateInsertTest_1')
	request.set_prompt('AttributeTemplateInsertTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateInsert)

	assert isinstance(response.get_attribute_template(), merchantapi.model.AttributeTemplate)
	assert response.get_attribute_template().get_code() == 'AttributeTemplateInsertTest_1'
	assert response.get_attribute_template().get_prompt() == 'AttributeTemplateInsertTest_1'

	check = helper.get_attribute_template('AttributeTemplateInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template().get_id()

def test_attribute_template_update():
	"""
	Tests the AttributeTemplate_Update API Call
	"""

	helper.provision_store('AttributeTemplate_Update.xml')

	attribute_template_update_test_update()


def attribute_template_update_test_update():
	request = merchantapi.request.AttributeTemplateUpdate(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateUpdateTest_1')
	request.set_code('AttributeTemplateUpdateTest_1_Updated')
	request.set_prompt('AttributeTemplateUpdateTest_1_Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateUpdate)

	check = helper.get_attribute_template('AttributeTemplateUpdateTest_1_Updated')

	assert check is not None
	assert check.get_code() == 'AttributeTemplateUpdateTest_1_Updated'
	assert check.get_prompt() == 'AttributeTemplateUpdateTest_1_Updated'


def test_attribute_template_delete():
	"""
	Tests the AttributeTemplate_Delete API Call
	"""

	helper.provision_store('AttributeTemplate_Delete.xml')

	attribute_template_delete_test_deletion()


def attribute_template_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateDelete(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateDeleteTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateDelete)

	check = helper.get_attribute_template('AttributeTemplateDeleteTest_1')

	assert check is None


def test_attribute_template_option_set_default():
	"""
	Tests the AttributeTemplateOption_Set_Default API Call
	"""

	helper.provision_store('AttributeTemplateOption_Set_Default.xml')

	attribute_template_option_set_default_test_set_default()


def attribute_template_option_set_default_test_set_default():
	request = merchantapi.request.AttributeTemplateOptionSetDefault(helper.init_client())

	request.set_attribute_template_code('ATOSD_Template_1')
	request.set_attribute_template_attribute_code('ATOSD_Attribute_1')
	request.set_attribute_template_option_code('ATOSD_Option_2')
	request.set_attribute_template_option_default(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionSetDefault)

	checkA = helper.get_attribute_template_attribute('ATOSD_Template_1', 'ATOSD_Attribute_1')
	checkO = helper.get_attribute_template_option('ATOSD_Template_1', 'ATOSD_Attribute_1', 'ATOSD_Option_2')

	assert checkA is not None
	assert checkO is not None
	assert checkA.get_default_id() == checkO.get_id()


def test_attribute_template_product_list_load_query():
	"""
	Tests the AttributeTemplateProductList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateProductList_Load_Query.xml')

	attribute_template_product_list_load_query_test_list_load()


def attribute_template_product_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductListTemplate')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(response.get_attribute_template_products()) > 0

	for p in response.get_attribute_template_products():
		assert 'AttributeTemplateProduct' in p.get_code()


def test_attribute_template_product_update_assigned():
	"""
	Tests the AttributeTemplateProduct_Update_Assigned API Call
	"""

	helper.provision_store('AttributeTemplateProduct_Update_Assigned.xml')

	attribute_template_product_update_assigned_test_assignment()
	attribute_template_product_update_assigned_test_unassignment()


def attribute_template_product_update_assigned_test_assignment():
	request = merchantapi.request.AttributeTemplateProductUpdateAssigned(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_1')
	request.set_product_code('AttributeTemplateProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductUpdateAssigned)

	check_request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())
	check_request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_1')
	check_request.set_filters(check_request.filter_expression().equal('code', 'AttributeTemplateProductUpdateAssignedTest_1'))
	check_request.set_assigned(True)
	check_request.set_unassigned(False)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(check_response.get_attribute_template_products()) == 1
	assert check_response.get_attribute_template_products()[0].get_assigned() is True


def attribute_template_product_update_assigned_test_unassignment():
	request = merchantapi.request.AttributeTemplateProductUpdateAssigned(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_2')
	request.set_product_code('AttributeTemplateProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductUpdateAssigned)

	check_request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())
	check_request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_2')
	check_request.set_filters(check_request.filter_expression().equal('code', 'AttributeTemplateProductUpdateAssignedTest_2'))
	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(check_response.get_attribute_template_products()) == 1
	assert check_response.get_attribute_template_products()[0].get_assigned() is False


def test_attribute_load_code():
	"""
	Tests the Attribute_Load_Code API Call
	"""

	helper.provision_store('Attribute_Load_Code.xml')

	attribute_load_code_test_load()


def attribute_load_code_test_load():
	request = merchantapi.request.AttributeLoadCode(helper.init_client())

	request.set_product_code('AttributeLoadCodeTest_1')
	request.set_attribute_code('attr_choice')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeLoadCode)

	assert response.get_product_attribute() is not None
	assert response.get_product_attribute().get_code() is not None


def test_attribute_insert():
	"""
	Tests the Attribute_Insert API Call
	"""

	helper.provision_store('Attribute_Insert.xml')

	attribute_insert_test_insertion()


def attribute_insert_test_insertion():
	request = merchantapi.request.AttributeInsert(helper.init_client())

	request.set_product_code("AttributeInsertTest_1")
	request.set_code('TestInsert1')
	request.set_prompt('TestInsert1')
	request.set_type('checkbox')
	request.set_image('')
	request.set_price(2.00)
	request.set_cost(1.00)
	request.set_weight(3.00)
	request.set_copy(False)
	request.set_required(False)
	request.set_inventory(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeInsert)

	assert isinstance(response.get_product_attribute(), merchantapi.model.ProductAttribute)
	assert response.get_product_attribute().get_prompt() == 'TestInsert1'

	check = helper.get_product_attribute('AttributeInsertTest_1', 'TestInsert1')

	assert check is not None
	assert check.get_id() == response.get_product_attribute().get_id()


def test_attribute_update():
	"""
	Tests the Attribute_Update API Call
	"""

	helper.provision_store('Attribute_Update.xml')

	attribute_update_test_update()


def attribute_update_test_update():
	request = merchantapi.request.AttributeUpdate(helper.init_client())

	request.set_product_code('AttributeUpdateTest_1')
	request.set_attribute_code('AttributeUpdateTest_1')
	request.set_prompt('AttributeUpdateTest_1_Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeUpdate)

	check = helper.get_product_attribute('AttributeUpdateTest_1', 'AttributeUpdateTest_1')

	assert check is not None
	assert check.get_prompt() == 'AttributeUpdateTest_1_Updated'


def test_attribute_delete():
	"""
	Tests the Attribute_Delete API Call
	"""

	helper.provision_store('Attribute_Delete.xml')

	attribute_delete_test_deletion()


def attribute_delete_test_deletion():
	request = merchantapi.request.AttributeDelete(helper.init_client())

	request.set_product_code('AttributeDeleteTest_1')
	request.set_attribute_code('AttributeDeleteTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeDelete)

	check = helper.get_product_attribute('AttributeDeleteTest_1', 'AttributeDeleteTest_1')

	assert check is None


def test_attribute_and_option_list_load_product():
	"""
	Tests the AttributeAndOptionList_Load_Product API Call
	"""

	helper.provision_store('AttributeAndOptionList_Load_Product.xml')

	attribute_and_option_list_load_product_test_list_load()


def attribute_and_option_list_load_product_test_list_load():
	request = merchantapi.request.AttributeAndOptionListLoadProduct(helper.init_client())

	request.set_product_code('AttributeAndOptionListLoadProductTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeAndOptionListLoadProduct)

	assert len(response.get_product_attributes()) == 3

	valid_codes = [
		'AttributeAndOptionListLoadProductTest_1',
		'AttributeAndOptionListLoadProductTest_2',
		'AttributeAndOptionListLoadProductTest_3'
	]

	for a in response.get_product_attributes():
		assert a.get_code() in valid_codes
		assert len(a.get_options()) == 3

		for o in a.get_options():
			assert o.get_code() in valid_codes


def test_availability_group_customer_list_load_query():
	"""
	Tests the AvailabilityGroupCustomerList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupCustomerList_Load_Query.xml')

	availability_group_customer_list_load_query_test_list_load()


def availability_group_customer_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupCustomerListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGCUSLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'AGCUSLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCustomerListLoadQuery)

	assert len(response.get_availability_group_customers()) == 5

	valid_logins = [
		'AGCUSLLoadQueryTest_1',
		'AGCUSLLoadQueryTest_2',
		'AGCUSLLoadQueryTest_3',
		'AGCUSLLoadQueryTest_4',
		'AGCUSLLoadQueryTest_5'
	]

	for c in response.get_availability_group_customers():
		assert c.get_login() in valid_logins


def test_availability_group_product_list_load_query():
	"""
	Tests the AvailabilityGroupProductList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupProductList_Load_Query.xml')

	availability_group_product_list_load_query_test_list_load()


def availability_group_product_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupProductListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGPRODLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'AGPRODLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductListLoadQuery)

	assert len(response.get_availability_group_products()) == 5

	valid_codes = [
		'AGPRODLLoadQueryTest_1',
		'AGPRODLLoadQueryTest_2',
		'AGPRODLLoadQueryTest_3',
		'AGPRODLLoadQueryTest_4',
		'AGPRODLLoadQueryTest_5'
	]

	for p in response.get_availability_group_products():
		assert p.get_code() in valid_codes


def test_availability_group_delete():
	"""
	Tests the AvailabilityGroup_Delete API Call
	"""

	helper.provision_store('AvailabilityGroup_Delete.xml')

	availability_group_delete_test_deletion()


def availability_group_delete_test_deletion():
	group = helper.get_availability_group('AvailabilityGroupDeleteTest_1')

	assert group is not None

	request = merchantapi.request.AvailabilityGroupDelete(helper.init_client(), group)

	assert request.get_availability_group_id() == group.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupDelete)

	check = helper.get_availability_group('AvailabilityGroupDeleteTest_1')

	assert check is None


def test_availability_group_insert():
	"""
	Tests the AvailabilityGroup_Insert API Call
	"""

	helper.provision_store('AvailabilityGroup_Insert.xml')

	availability_group_insert_test_insertion()


def availability_group_insert_test_insertion():
	group = helper.get_availability_group('AvailabilityGroupInsertTest_1')

	assert group is None

	request = merchantapi.request.AvailabilityGroupInsert(helper.init_client())

	request.set_availability_group_name('AvailabilityGroupInsertTest_1')
	request.set_availability_group_tax_exempt(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupInsert)

	assert isinstance(response.get_availability_group(), merchantapi.model.AvailabilityGroup)
	assert response.get_availability_group().get_name() == 'AvailabilityGroupInsertTest_1'
	assert response.get_availability_group().get_tax_exempt() is True

	check = helper.get_availability_group('AvailabilityGroupInsertTest_1')
	assert check is not None
	assert check.get_id() == response.get_availability_group().get_id()


def test_availability_group_update():
	"""
	Tests the AvailabilityGroup_Update API Call
	"""

	helper.provision_store('AvailabilityGroup_Update.xml')

	availability_group_update_test_update()


def availability_group_update_test_update():
	group = helper.get_availability_group('AvailabilityGroupUpdateTest_1')

	assert group is not None

	request = merchantapi.request.AvailabilityGroupUpdate(helper.init_client(), group)

	request.set_availability_group_name('AvailabilityGroupUpdateTest_1_Modified')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupUpdate)

	checkA = helper.get_availability_group('AvailabilityGroupUpdateTest_1')
	checkB = helper.get_availability_group('AvailabilityGroupUpdateTest_1_Modified')

	assert checkA is None
	assert checkB is not None


def test_availability_group_category_list_load_query():
	"""
	Tests the AvailabilityGroupCategoryList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupCategoryList_Load_Query.xml')

	availability_group_category_list_load_query_test_list_load()


def availability_group_category_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupCategoryListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGCATLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'AGCATLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryListLoadQuery)

	valid_codes = [
		'AGCATLLoadQueryTest_1',
		'AGCATLLoadQueryTest_2',
		'AGCATLLoadQueryTest_3',
		'AGCATLLoadQueryTest_4',
		'AGCATLLoadQueryTest_5'
	]

	assert len(response.get_availability_group_categories()) == 5

	for c in response.get_availability_group_categories():
		assert c.get_code() in valid_codes


def test_availability_group_category_update_assigned():
	"""
	Tests the AvailabilityGroupCategory_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupCategory_Update_Assigned.xml')

	availability_group_category_update_assigned_test_assignment()
	availability_group_category_update_assigned_test_unassignment()


def availability_group_category_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupCategoryUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCatUpdateAssignedTest')
	request.set_category_code('AvailabilityGrpCatUpdateAssignedTest_Cat2')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryUpdateAssigned)

	check = helper.get_availability_group_categories('AvailabilityGrpCatUpdateAssignedTest', 'AvailabilityGrpCatUpdateAssignedTest_Cat2', True, False)

	assert len(check) == 1


def availability_group_category_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupCategoryUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCatUpdateAssignedTest')
	request.set_category_code('AvailabilityGrpCatUpdateAssignedTest_Cat1')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryUpdateAssigned)

	check = helper.get_availability_group_categories('AvailabilityGrpCatUpdateAssignedTest', 'AvailabilityGrpCatUpdateAssignedTest_Cat1', False, True)

	assert len(check) == 1


def test_availability_group_business_account_list_load_query():
	"""
	Tests the AvailabilityGroupBusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupBusinessAccountList_Load_Query.xml')

	availability_group_business_account_list_load_query_test_list_load()


def availability_group_business_account_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupBusinessAccountListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGBALLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('title', 'AGBALLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountListLoadQuery)

	valid_titles = [
		'AGBALLoadQueryTest_1',
		'AGBALLoadQueryTest_2',
		'AGBALLoadQueryTest_3',
		'AGBALLoadQueryTest_4',
		'AGBALLoadQueryTest_5',
	]

	assert len(response.get_availability_group_business_accounts()) == 5

	for b in response.get_availability_group_business_accounts():
		assert b.get_title() in valid_titles


def test_availability_group_shipping_method_list_load_query():
	"""
	Tests the AvailabilityGroupShippingMethodList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupShippingMethodList_Load_Query.xml')

	availability_group_shipping_method_list_load_query_test_list_load()


def availability_group_shipping_method_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupShippingMethodListLoadQuery(helper.init_client())

	request.set_availability_group_name('AvailGroupShpMthdListLoadQueryTest')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodListLoadQuery)

	valid_codes = [
		'AvailGroupShpMthdListLoadQuery1',
		'AvailGroupShpMthdListLoadQuery2',
		'AvailGroupShpMthdListLoadQuery3',
		'AvailGroupShpMthdListLoadQuery4',
		'AvailGroupShpMthdListLoadQuery5',
	]

	assert len(response.get_availability_group_shipping_methods()) == 5

	for s in response.get_availability_group_shipping_methods():
		assert s.get_method_code() in valid_codes

def test_branch_set_primary():
	"""
	Tests the Branch_SetPrimary API Call
	"""

	branch_set_primary_test_set_primary()


def branch_set_primary_test_set_primary():
	helper.delete_branch('Production Copy')

	base_branch = helper.get_branch('Production')

	branch = helper.create_branch('Production Copy', '#000000', base_branch)

	assert branch is not None

	request = merchantapi.request.BranchSetPrimary(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchSetPrimary)

	# Reset back to default primary or other tests might fail
	request.set_branch_id(base_branch.get_id())
	request.send()


def test_branch_update():
	"""
	Tests the Branch_Update API Call
	"""

	branch_update_test_update()


def branch_update_test_update():
	helper.delete_branch('Production Copy')

	base_branch = helper.get_branch('Production')

	branch = helper.create_branch('Production Copy', '#000000', base_branch)

	assert branch is not None

	request = merchantapi.request.BranchUpdate(helper.init_client(), branch)

	request.set_branch_color('#f1f1f1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchUpdate)

	check_branch = helper.get_branch('Production Copy')

	assert check_branch is not None
	assert check_branch.get_color() == '#f1f1f1'


def test_business_account_list_load_query():
	"""
	Tests the BusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('BusinessAccountList_Load_Query.xml')

	business_account_list_load_query_test_list_load()


def business_account_list_load_query_test_list_load():
	request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('title', 'BusinessAccountListLoadQueryTest%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountListLoadQuery)

	assert len(response.get_business_accounts()) == 7


def test_business_account_insert():
	"""
	Tests the BusinessAccount_Insert API Call
	"""

	helper.provision_store('BusinessAccount_Insert.xml')

	business_account_insert_test_insertion()


def business_account_insert_test_insertion():
	existing = helper.get_business_account('BusinessAccountInsertTest_1')

	assert existing is None

	request = merchantapi.request.BusinessAccountInsert(helper.init_client())

	request.set_business_account_title('BusinessAccountInsertTest_1')
	request.set_business_account_tax_exempt(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountInsert)
	
	assert isinstance(response.get_business_account(), merchantapi.model.BusinessAccount)
	assert response.get_business_account().get_title() == 'BusinessAccountInsertTest_1'
	assert response.get_business_account().get_tax_exempt() == True

	check = helper.get_business_account('BusinessAccountInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_business_account().get_id()


def test_business_account_update():
	"""
	Tests the BusinessAccount_Update API Call
	"""

	helper.provision_store('BusinessAccount_Update.xml')

	business_account_update_test_update()


def business_account_update_test_update():
	existing = helper.get_business_account('BusinessAccountUpdateTest_1')

	assert existing is not None

	request = merchantapi.request.BusinessAccountUpdate(helper.init_client(), existing)

	request.set_business_account_title('BusinessAccountUpdateTest_1_Modified')
	request.set_business_account_tax_exempt(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountUpdate)

	check = helper.get_business_account('BusinessAccountUpdateTest_1_Modified')

	assert check is not None
	assert check.get_title() == 'BusinessAccountUpdateTest_1_Modified'
	assert check.get_tax_exempt() == False


def test_business_account_list_delete():
	"""
	Tests the BusinessAccountList_Delete API Call
	"""

	helper.provision_store('BusinessAccountList_Delete.xml')

	business_account_list_delete_test_deletion()


def business_account_list_delete_test_deletion():
	list_request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())
	list_request.set_filters(list_request.filter_expression().like('title', 'BusinessAccountListDeleteTest%'))
	list_response = list_request.send()

	assert len(list_response.get_business_accounts()) == 3

	request = merchantapi.request.BusinessAccountListDelete(helper.init_client())

	for a in list_response.get_business_accounts():
		request.add_business_account(a)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountListDelete)

	check_list_request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())
	check_list_request.set_filters(check_list_request.filter_expression().like('title', 'BusinessAccountListDeleteTest%'))
	check_list_response = check_list_request.send()

	assert len(check_list_response.get_business_accounts())  == 0


def test_business_account_customer_list_load_query():
	"""
	Tests the BusinessAccountCustomerList_Load_Query API Call
	"""

	helper.provision_store('BusinessAccountCustomerList_Load_Query.xml')

	business_account_customer_list_load_query_test_list_load_assigned()
	business_account_customer_list_load_query_test_list_load_unassigned()


def business_account_customer_list_load_query_test_list_load_assigned():
	request = merchantapi.request.BusinessAccountCustomerListLoadQuery(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'BusinessAccountCustomerListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerListLoadQuery)

	assert len(response.get_business_account_customers()) == 5


def business_account_customer_list_load_query_test_list_load_unassigned():
	request = merchantapi.request.BusinessAccountCustomerListLoadQuery(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'BusinessAccountCustomerListLoadQueryTest%'))
	request.set_assigned(False)
	request.set_unassigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerListLoadQuery)

	assert len(response.get_business_account_customers()) == 1


def test_business_account_customer_update_assigned():
	"""
	Tests the BusinessAccountCustomer_Update_Assigned API Call
	"""

	helper.provision_store('BusinessAccountCustomer_Update_Assigned.xml')

	business_account_customer_update_assigned_test_assignment()
	business_account_customer_update_assigned_test_unassignment()


def business_account_customer_update_assigned_test_assignment():
	request = merchantapi.request.BusinessAccountCustomerUpdateAssigned(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_customer_login('BusinessAccountCustomerUpdateAssignedTest_2')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerUpdateAssigned)

	check = helper.get_customer_business_account('BusinessAccountCustomerUpdateAssignedTest_1', 'BusinessAccountCustomerUpdateAssignedTest_2', True, False)
	assert len(check) == 1


def business_account_customer_update_assigned_test_unassignment():
	request = merchantapi.request.BusinessAccountCustomerUpdateAssigned(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_customer_login('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerUpdateAssigned)

	check = helper.get_customer_business_account('BusinessAccountCustomerUpdateAssignedTest_1', 'BusinessAccountCustomerUpdateAssignedTest_1', False, True)
	assert len(check) == 1


def test_category_uri_insert():
	"""
	Tests the CategoryURI_Insert API Call
	"""

	helper.provision_store('CategoryURI_Insert.xml')

	category_uri_insert_test_insertion()


def category_uri_insert_test_insertion():
	test_uri = '/CategoryURIInsertTest_1_1'
	category = helper.get_category('CategoryURIInsertTest_1')

	assert category is not None

	request = merchantapi.request.CategoryURIInsert(helper.init_client(), category)

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_category('CategoryURIInsertTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_category_uri_update():
	"""
	Tests the CategoryURI_Update API Call
	"""

	helper.provision_store('CategoryURI_Update.xml')

	category_uri_update_test_update()


def category_uri_update_test_update():
	category = helper.get_category('CategoryURIUpdateTest_1')

	assert category is not None
	assert len(category.get_uris()) == 2

	uri = None

	for u in category.get_uris():
		if u.get_canonical():
			continue
		uri = u
		break

	assert uri is not None

	test_uri = uri.get_uri() + '_1_1'

	request = merchantapi.request.CategoryURIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIUpdate)

	check = helper.get_category('CategoryURIUpdateTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_category_uri_list_load_query():
	"""
	Tests the CategoryURIList_Load_Query API Call
	"""

	helper.provision_store('CategoryURIList_Load_Query.xml')

	category_uri_list_load_query_test_list_load()


def category_uri_list_load_query_test_list_load():
	category = helper.get_category('CategoryURIListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.CategoryURIListLoadQuery(helper.init_client(), category)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIListLoadQuery)

	assert len(response.get_uris()) > 1

	for uri in response.get_uris():
		assert uri.get_category_id() == category.get_id()
		if uri.get_canonical():
			continue
		assert 'CategoryURIListLoadQueryTest' in uri.get_uri()


def test_category_uri_list_delete():
	"""
	Tests the CategoryURIList_Delete API Call
	"""

	helper.provision_store('CategoryURIList_Delete.xml')

	category_uri_list_delete_test_deletion()


def category_uri_list_delete_test_deletion():
	category = helper.get_category('CategoryURIListDeleteTest_1')

	assert category is not None
	assert len(category.get_uris()) > 1

	request = merchantapi.request.CategoryURIListDelete(helper.init_client())

	for u in category.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIListDelete)

	check = helper.get_category('CategoryURIListDeleteTest_1')

	assert check is not None
	assert len(check.get_uris()) == 1


def test_category_uri_redirect():
	"""
	Tests the CategoryURI_Redirect API Call
	"""

	helper.provision_store('CategoryURI_Redirect.xml')

	category_uri_redirect_test_redirect()


def category_uri_redirect_test_redirect():
	category_a = helper.get_category('CategoryURIRedirectTest_1')
	category_b = helper.get_category('CategoryURIRedirectTest_2')

	assert category_a is not None
	assert category_b is not None
	assert len(category_a.get_uris()) == 3
	assert len(category_b.get_uris()) == 3

	request = merchantapi.request.CategoryURIRedirect(helper.init_client())

	request.set_destination(category_a.get_code())
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('category')
	request.set_status(301)

	for u in category_b.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIRedirect)

	category_b_check = helper.get_category('CategoryURIRedirectTest_2')

	assert category_b_check is not None
	assert len(category_b_check.get_uris()) == 1


def test_child_category_list_load_query():
	"""
	Tests the ChildCategoryList_Load_Query API Call
	"""

	helper.provision_store('ChildCategoryList_Load_Query.xml')

	child_category_list_load_query_test_list_load_assigned()
	child_category_list_load_query_test_list_load_assigned_code()
	child_category_list_load_query_test_list_load_unassigned()


def child_category_list_load_query_test_list_load_assigned():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client(), category)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert request.get_parent_category_id() > 0

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 6


def child_category_list_load_query_test_list_load_assigned_code():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client())

	request.set_parent_category_code('ChildCategoryListLoadQueryTest_1')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 6


def child_category_list_load_query_test_list_load_unassigned():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client(), category)

	request.set_filters(request.filter_expression().like('code', 'ChildCategoryListLoadQueryTest%'))
	request.set_assigned(False)
	request.set_unassigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 2


def test_coupon_customer_list_load_query():
	"""
	Tests the CouponCustomerList_Load_Query API Call
	"""

	helper.provision_store('CouponCustomerList_Load_Query.xml')

	coupon_customer_list_load_query_test_list_load()


def coupon_customer_list_load_query_test_list_load():
	coupon = helper.get_coupon('CouponCustomerListLoadQueryTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerListLoadQuery(helper.init_client(), coupon)

	request.set_filters(request.filter_expression().like('login', 'CouponCustomerListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerListLoadQuery)

	assert len(response.get_coupon_customers()) == 5


def test_coupon_customer_update_assigned():
	"""
	Tests the CouponCustomer_Update_Assigned API Call
	"""

	helper.provision_store('CouponCustomer_Update_Assigned.xml')

	coupon_customer_update_assigned_test_assignment()
	coupon_customer_update_assigned_test_unassignment()


def coupon_customer_update_assigned_test_assignment():
	coupon = helper.get_coupon('CouponCustomerUpdateAssignedTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerUpdateAssigned(helper.init_client(), coupon)

	request.set_customer_login('CouponCustomerUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerUpdateAssigned)

	check = helper.get_coupon_customers('CouponCustomerUpdateAssignedTest_1', 'CouponCustomerUpdateAssignedTest_1', True, False)

	assert check is not None
	assert len(check) == 1


def coupon_customer_update_assigned_test_unassignment():
	coupon = helper.get_coupon('CouponCustomerUpdateAssignedTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerUpdateAssigned(helper.init_client(), coupon)

	request.set_customer_login('CouponCustomerUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerUpdateAssigned)

	check = helper.get_coupon_customers('CouponCustomerUpdateAssignedTest_1', 'CouponCustomerUpdateAssignedTest_2', False, True)

	assert check is not None
	assert len(check) == 1


def test_customer_address_insert():
	"""
	Tests the CustomerAddress_Insert API Call
	"""

	helper.provision_store('CustomerAddress_Insert.xml')

	customer_address_insert_test_insertion()


def customer_address_insert_test_insertion():
	customer = helper.get_customer('CustomerAddressInsertTest')
	addresses = helper.get_customer_addresses('CustomerAddressInsertTest')

	assert customer is not None
	assert addresses is not None
	assert len(addresses) >= 1

	request = merchantapi.request.CustomerAddressInsert(helper.init_client(), customer)

	request.set_description('CustomerAddressInsertTest')
	request.set_first_name('Insert')
	request.set_last_name('Test')
	request.set_email('test@coolcommerce.net')
	request.set_phone('1231231234')
	request.set_fax('3213214321')
	request.set_company('Miva Inc')
	request.set_address1('1234 Miva St')
	request.set_address2('Ste 1')
	request.set_city('San Diego')
	request.set_state('CA')
	request.set_zip('92009')
	request.set_country('US')
	request.set_residential(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressInsert)

	assert isinstance(response.get_customer_address(), merchantapi.model.CustomerAddress)
	assert response.get_customer_address().get_description() == 'CustomerAddressInsertTest'
	assert response.get_customer_address().get_first_name() == 'Insert'
	assert response.get_customer_address().get_last_name() == 'Test'
	assert response.get_customer_address().get_email() == 'test@coolcommerce.net'
	assert response.get_customer_address().get_phone() == '1231231234'
	assert response.get_customer_address().get_fax() == '3213214321'
	assert response.get_customer_address().get_company() == 'Miva Inc'
	assert response.get_customer_address().get_address1() == '1234 Miva St'
	assert response.get_customer_address().get_address2() == 'Ste 1'
	assert response.get_customer_address().get_city() == 'San Diego'
	assert response.get_customer_address().get_state() == 'CA'
	assert response.get_customer_address().get_zip() == '92009'
	assert response.get_customer_address().get_country() == 'US'
	assert response.get_customer_address().get_residential() is True

	address = None
	for a in helper.get_customer_addresses('CustomerAddressInsertTest'):
		if a.get_description() == 'CustomerAddressInsertTest':
			address = a
			break

	assert address is not None
	assert address.get_id() == response.get_customer_address().get_id()


def test_customer_address_update():
	"""
	Tests the CustomerAddress_Update API Call
	"""

	helper.provision_store('CustomerAddress_Update.xml')

	customer_address_update_test_update()


def customer_address_update_test_update():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateTest'):
		if a.get_description() == 'CustomerAddressUpdateTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressUpdate(helper.init_client(), address)

	request.set_description(address.get_description() + ' UPDATED')
	request.set_first_name(address.get_first_name() + ' UPDATED')
	request.set_last_name(address.get_last_name() + ' UPDATED')
	request.set_email(address.get_email() + '.up')
	request.set_phone(address.get_phone() + '1')
	request.set_fax(address.get_fax() + '1')
	request.set_company(address.get_company() + ' UPDATED')
	request.set_address1(address.get_address1() + ' UPDATED')
	request.set_address2(address.get_address2() + ' UPDATED')
	request.set_city(address.get_city() + ' UPDATED')
	request.set_state(address.get_state() + ' UPDATED')
	request.set_zip(address.get_zip() + ' UPDATED')
	request.set_country(address.get_country() + ' UPDATED')
	request.set_residential(not address.get_residential())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressUpdate)

	check_address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateTest'):
		if a.get_id() == address.get_id():
			check_address = a
			break

	assert check_address is not None
	assert address.get_description() != check_address.get_description()
	assert address.get_first_name() != check_address.get_first_name()
	assert address.get_last_name() != check_address.get_last_name()
	assert address.get_email() != check_address.get_email()
	assert address.get_phone() != check_address.get_phone()
	assert address.get_fax() != check_address.get_fax()
	assert address.get_company() != check_address.get_company()
	assert address.get_address1() != check_address.get_address1()
	assert address.get_address2() != check_address.get_address2()
	assert address.get_city() != check_address.get_city()
	assert address.get_state() != check_address.get_state()
	assert address.get_zip() != check_address.get_zip()
	assert address.get_country() != check_address.get_country()
	assert address.get_residential() != check_address.get_residential()


def test_customer_address_delete():
	"""
	Tests the CustomerAddress_Delete API Call
	"""

	helper.provision_store('CustomerAddress_Delete.xml')

	customer_address_delete_test_deletion()


def customer_address_delete_test_deletion():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressDeleteTest'):
		if a.get_description() == 'CustomerAddressDeleteTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressDelete(helper.init_client())

	request.set_customer_login('CustomerAddressDeleteTest')
	request.set_customer_address_id(address.get_id())
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressDelete)

	check = None
	for a in helper.get_customer_addresses('CustomerAddressDeleteTest'):
		if a.get_id() == address.get_id():
			check = a
			break

	assert check is None


def test_customer_address_list_delete():
	"""
	Tests the CustomerAddressList_Delete API Call
	"""

	helper.provision_store('CustomerAddressList_Delete.xml')

	customer_address_list_delete_test_deletion()


def customer_address_list_delete_test_deletion():
	addresses = helper.get_customer_addresses('CustomerAddressListDeleteTest')
	assert addresses is not None
	assert len(addresses) >= 3

	request = merchantapi.request.CustomerAddressListDelete(helper.init_client())

	request.set_customer_login('CustomerAddressListDeleteTest')

	for a in addresses:
		request.add_customer_address(a)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListDelete)

	check = helper.get_customer_addresses('CustomerAddressListDeleteTest')

	assert len(check) == 0


def test_customer_address_update_residential():
	"""
	Tests the CustomerAddress_Update_Residential API Call
	"""

	helper.provision_store('CustomerAddress_Update_Residential.xml')

	customer_address_update_residential_test_update()


def customer_address_update_residential_test_update():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateResidentialTest'):
		if a.get_description() == 'CustomerAddressUpdateResidentialTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressUpdateResidential(helper.init_client())

	request.set_customer_address_id(address.get_id())
	request.set_residential(not address.get_residential())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressUpdateResidential)

	check_address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateResidentialTest'):
		if a.get_id() == address.get_id():
			check_address = a
			break

	assert check_address is not None
	assert check_address.get_residential() != address.get_residential()


def test_feed_uri_insert():
	"""
	Tests the FeedURI_Insert API Call
	"""

	helper.provision_store('FeedURI_Insert.xml')

	feed_uri_insert_test_insertion()


def feed_uri_insert_test_insertion():
	test_uri = '/FeedURIInsertTest_1_INSERTED'

	request = merchantapi.request.FeedURIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_feed_code('FeedURIInsertTest_1')
	request.set_canonical(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_feed_uris('FeedURIInsertTest_1')

	assert len(check) == 1
	assert check[0].get_uri() == test_uri


def test_feed_uri_update():
	"""
	Tests the FeedURI_Update API Call
	"""

	helper.provision_store('FeedURI_Update.xml')

	feed_uri_update_test_update()


def feed_uri_update_test_update():
	uris = helper.get_feed_uris('FeedURIUpdateTest_1')

	assert len(uris) == 1

	test_uri = uris[0].get_uri() + '_UPDATED'

	request = merchantapi.request.FeedURIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIUpdate)

	check = helper.get_feed_uris('FeedURIUpdateTest_1')

	assert len(check) == 1
	assert check[0].get_uri() == test_uri


def test_feed_uri_list_load_query():
	"""
	Tests the FeedURIList_Load_Query API Call
	"""

	helper.provision_store('FeedURIList_Load_Query.xml')

	feed_uri_list_load_query_test_list_load()


def feed_uri_list_load_query_test_list_load():
	request = merchantapi.request.FeedURIListLoadQuery(helper.init_client())

	request.set_feed_code('FeedURIListLoadQueryTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIListLoadQuery)

	assert len(response.get_uris()) == 8


def test_feed_uri_list_delete():
	"""
	Tests the FeedURIList_Delete API Call
	"""

	helper.provision_store('FeedURIList_Delete.xml')

	feed_uri_list_delete_test_deletion()


def feed_uri_list_delete_test_deletion():
	uris = helper.get_feed_uris('FeedURIListDeleteTest_1')

	assert uris is not None
	assert len(uris) == 8

	request = merchantapi.request.FeedURIListDelete(helper.init_client())

	for u in uris:
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIListDelete)

	check = helper.get_feed_uris('FeedURIListDeleteTest_1')

	assert len(check) == 0


def test_image_type_list_load_query():
	"""
	Tests the ImageTypeList_Load_Query API Call
	"""

	helper.provision_store('ImageTypeList_Load_Query.xml')

	image_type_list_load_query_test_list_load()


def image_type_list_load_query_test_list_load():
	request = merchantapi.request.ImageTypeListLoadQuery(helper.init_client())
	request.set_filters(request.filter_expression().like('code', 'ImageTypeListLoadQueryTest%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ImageTypeListLoadQuery)

	assert len(response.get_image_types()) == 5


def test_inventory_product_settings_update():
	"""
	Tests the InventoryProductSettings_Update API Call
	"""

	helper.provision_store('InventoryProductSettings_Update.xml')

	inventory_product_settings_update_test_update()


def inventory_product_settings_update_test_update():
	product = helper.get_product('InventoryProductSettingsUpdateTest_1');

	assert product is not None

	request = merchantapi.request.InventoryProductSettingsUpdate(helper.init_client(), product)

	request.set_track_product(True)
	request.set_track_low_stock_level("Yes")
	request.set_track_out_of_stock_level("Yes")
	request.set_hide_out_of_stock_products("Yes")
	request.set_in_stock_message_short("It is in stock")
	request.set_in_stock_message_long("Stop complaining, we can ship it right now")
	request.set_low_stock_message_short("Speak now")
	request.set_low_stock_message_long("Or forever hold your peace")
	request.set_out_of_stock_message_short("Sucker")
	request.set_out_of_stock_message_long("We sold out because you waited too long")
	request.set_limited_stock_message("We have of the limited")
	request.set_current_stock(12);

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.InventoryProductSettingsUpdate)

	check = helper.get_product(product.get_code());

	assert check.get_product_inventory_settings().get_in_stock_message_short() ==  "It is in stock"
	assert check.get_product_inventory_settings().get_in_stock_message_long() ==  "Stop complaining, we can ship it right now"
	assert check.get_product_inventory_settings().get_low_stock_message_short() ==  "Speak now"
	assert check.get_product_inventory_settings().get_low_stock_message_long() ==  "Or forever hold your peace"
	assert check.get_product_inventory_settings().get_out_of_stock_message_short() ==  "Sucker"
	assert check.get_product_inventory_settings().get_out_of_stock_message_long() ==  "We sold out because you waited too long"
	assert check.get_product_inventory_settings().get_limited_stock_message() ==  "We have of the limited"

def test_option_list_load_attribute():
	"""
	Tests the OptionList_Load_Attribute API Call
	"""

	helper.provision_store('OptionList_Load_Attribute.xml')

	option_list_load_attribute_test_load()


def option_list_load_attribute_test_load():
	request = merchantapi.request.OptionListLoadAttribute(helper.init_client())

	request.set_product_code('OptionListLoadAttributeTest_1')
	request.set_attribute_code('OptionListLoadAttributeTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionListLoadAttribute)

	assert len(response.get_product_options()) == 2
	assert response.get_product_options()[0].get_code() == 'OptionListLoadAttributeTest_1'
	assert response.get_product_options()[1].get_code() == 'OptionListLoadAttributeTest_2'


def test_option_delete():
	"""
	Tests the Option_Delete API Call
	"""

	helper.provision_store('Option_Delete.xml')

	option_delete_test_deletion()


def option_delete_test_deletion():
	attribute = helper.get_product_attribute('OptionDeleteTest_1', 'OptionDeleteTest_1')
	options = helper.get_product_options('OptionDeleteTest_1', 'OptionDeleteTest_1')

	assert attribute is not None
	assert len(options) == 2

	request = merchantapi.request.OptionDelete(helper.init_client())

	request.set_option_code('OptionDeleteTest_1')
	request.set_attribute_id(attribute.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionDelete)

	check_options = helper.get_product_options('OptionDeleteTest_1', 'OptionDeleteTest_1')

	assert len(check_options) == 1


def test_option_insert():
	"""
	Tests the Option_Insert API Call
	"""

	helper.provision_store('Option_Insert.xml')

	option_insert_test_insertion()


def option_insert_test_insertion():
	options = helper.get_product_options('OptionInsertTest_1', 'OptionInsertTest_1')

	assert len(options) == 0

	request = merchantapi.request.OptionInsert(helper.init_client())

	request.set_product_code('OptionInsertTest_1')
	request.set_attribute_code('OptionInsertTest_1')
	request.set_code('OptionInsertTest_1')
	request.set_prompt('OptionInsertTest_1')
	request.set_image('')
	request.set_price(5.00)
	request.set_cost(2.2)
	request.set_weight(1.1)
	request.set_default(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionInsert)

	assert isinstance(response.get_product_option(), merchantapi.model.ProductOption)
	assert response.get_product_option().get_code() == 'OptionInsertTest_1'
	assert response.get_product_option().get_prompt() == 'OptionInsertTest_1'
	assert response.get_product_option().get_image() == ''
	assert response.get_product_option().get_price() == 5.00
	assert response.get_product_option().get_cost() == 2.2
	assert response.get_product_option().get_weight() == 1.1

	check_options = helper.get_product_options('OptionInsertTest_1', 'OptionInsertTest_1')

	assert len(check_options) == 1
	assert check_options[0].get_id() == response.get_product_option().get_id()


def test_option_update():
	"""
	Tests the Option_Update API Call
	"""

	helper.provision_store('Option_Update.xml')

	option_update_test_update()


def option_update_test_update():
	attribute = helper.get_product_attribute('OptionUpdateTest_1', 'OptionUpdateTest_1')
	options = helper.get_product_options('OptionUpdateTest_1', 'OptionUpdateTest_1')

	assert attribute is not None
	assert len(options) == 1

	request = merchantapi.request.OptionUpdate(helper.init_client())

	request.set_product_code('OptionUpdateTest_1')
	request.set_option_code('OptionUpdateTest_1')
	request.set_attribute_id(attribute.get_id())
	request.set_prompt('OptionUpdateTest_1 Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionUpdate)

	check_options = helper.get_product_options('OptionUpdateTest_1', 'OptionUpdateTest_1')

	assert len(check_options) == 1
	assert check_options[0].get_prompt() == 'OptionUpdateTest_1 Updated'


def test_option_load_code():
	"""
	Tests the Option_Load_Code API Call
	"""

	helper.provision_store('Option_Load_Code.xml')

	option_load_code_test_load()


def option_load_code_test_load():
	request = merchantapi.request.OptionLoadCode(helper.init_client())

	request.set_product_code('OptionLoadCodeTest_1')
	request.set_attribute_code('OptionLoadCodeTest_1')
	request.set_option_code('OptionLoadCodeTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionLoadCode)

	assert response.get_product_option() is not None
	assert response.get_product_option().get_code() == 'OptionLoadCodeTest_1'


def test_option_set_default():
	"""
	Tests the Option_Set_Default API Call
	"""

	helper.provision_store('Option_Set_Default.xml')

	option_set_default_test_set()


def option_set_default_test_set():
	attribute = helper.get_product_attribute('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1')

	assert attribute is not None

	request = merchantapi.request.OptionSetDefault(helper.init_client())

	request.set_attribute_id(attribute.get_id())
	request.set_option_code('OptionSetDefaultTest_2')
	request.set_option_default(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionSetDefault)

	check_attribute = helper.get_product_attribute('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1')
	check_option = None

	for o in helper.get_product_options('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1'):
		if o.get_code() == 'OptionSetDefaultTest_2':
			check_option = o
			break

	assert check_option is not None
	assert check_attribute.get_default_id() == check_option.get_id()


def test_order_item_split():
	"""
	Tests the OrderItem_Split API Call
	"""

	helper.provision_store('OrderItem_Split.xml')

	option_item_split_test_split()


def option_item_split_test_split():
	order = helper.get_order(895955)

	assert order is not None
	assert len(order.get_items()) == 1
	assert order.get_items()[0].get_quantity() == 4

	request = merchantapi.request.OrderItemSplit(helper.init_client())

	request.set_order_id(order.get_id())
	request.set_line_id(order.get_items()[0].get_line_id())
	request.set_quantity(2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemSplit)

	check_order = helper.get_order(order.get_id())

	assert len(check_order.get_items()) == 2
	assert check_order.get_items()[0].get_quantity() == 2
	assert check_order.get_items()[1].get_quantity() == 2


def test_order_item_list_remove_from_shipment():
	"""
	Tests the OrderItemList_RemoveFromShipment API Call
	"""

	helper.provision_store('OrderItemList_RemoveFromShipment.xml')

	order_item_list_remove_from_shipment_test_remove()


def order_item_list_remove_from_shipment_test_remove():
	order = helper.get_order(855855)

	assert order is not None
	assert len(order.get_items()) == 4

	shipments = helper.get_order_shipments(order.get_id())

	assert len(shipments) == 1

	request = merchantapi.request.OrderItemListRemoveFromShipment(helper.init_client(), order)

	request.add_order_item(order.get_items()[0])
	request.add_order_item(order.get_items()[1])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListRemoveFromShipment)

	check_order = helper.get_order(order.get_id())

	assert shipments[0].get_id() != check_order.get_items()[0].get_shipment_id()
	assert shipments[0].get_id() != check_order.get_items()[1].get_shipment_id()


def test_order_shipment_list_load_query():
	"""
	Tests the OrderShipmentList_Load_Query API Call
	"""

	helper.provision_store('OrderShipmentList_Load_Query.xml')

	order_shipment_list_load_query_test_list_load()
	order_shipment_list_load_query_test_list_load_filtered()


def order_shipment_list_load_query_test_list_load():
	request = merchantapi.request.OrderShipmentListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListLoadQuery)

	assert len(response.get_order_shipments()) > 0


def order_shipment_list_load_query_test_list_load_filtered():
	valid_ids = [855855, 855856, 855857, 855858, 855859, 855860]

	request = merchantapi.request.OrderShipmentListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().is_in('order_id', valid_ids))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListLoadQuery)

	assert len(response.get_order_shipments()) == 6

	for s in response.get_order_shipments():
		assert s.get_order_id() in valid_ids


def test_page_uri_insert():
	"""
	Tests the PageURI_Insert API Call
	"""

	helper.provision_store('PageURI_Insert.xml')

	page_uri_insert_test_insertion()


def page_uri_insert_test_insertion():
	test_uri = '/PageURIInsertTest_1_1'
	uris = helper.get_page_uris('PageURIInsertTest_1')

	assert len(uris) == 1

	request = merchantapi.request.PageURIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_page_code('PageURIInsertTest_1')
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_page_uris('PageURIInsertTest_1')
	uri = None

	for u in check:
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_page_uri_update():
	"""
	Tests the PageURI_Update API Call
	"""

	helper.provision_store('PageURI_Update.xml')

	page_uri_update_test_update()


def page_uri_update_test_update():
	uris = helper.get_page_uris('PageURIUpdateTest_1')

	assert len(uris) == 2

	test_uri = '/PageURIUpdateTest_1_1_1'

	request = merchantapi.request.PageURIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIUpdate)

	check = helper.get_page_uris('PageURIUpdateTest_1')

	uri = None
	for u in check:
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_page_uri_list_load_query():
	"""
	Tests the PageURIList_Load_Query API Call
	"""

	helper.provision_store('PageURIList_Load_Query.xml')

	page_uri_list_load_query_test_list_load()


def page_uri_list_load_query_test_list_load():
	request = merchantapi.request.PageURIListLoadQuery(helper.init_client())

	request.set_page_code('PageURIListLoadQueryTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIListLoadQuery)

	assert len(response.get_uris()) == 7


def test_page_uri_list_delete():
	"""
	Tests the PageURIList_Delete API Call
	"""

	helper.provision_store('PageURIList_Delete.xml')

	page_uri_list_delete_test_deletion()


def page_uri_list_delete_test_deletion():
	uris = helper.get_page_uris('PageURIListDeleteTest_1')

	assert uris is not None
	assert len(uris) == 7

	request = merchantapi.request.PageURIListDelete(helper.init_client())

	for u in uris:
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIListDelete)

	check = helper.get_page_uris('PageURIListDeleteTest_1')

	assert len(check) == 1


def test_page_uri_redirect():
	"""
	Tests the PageURI_Redirect API Call
	"""

	helper.provision_store('PageURI_Redirect.xml')

	page_uri_redirect_test_redirect()


def page_uri_redirect_test_redirect():
	page_a_uris = helper.get_page_uris('PageURIRedirectTest_1')
	page_b_uris = helper.get_page_uris('PageURIRedirectTest_2')

	assert len(page_a_uris) == 3
	assert len(page_b_uris) == 3

	request = merchantapi.request.PageURIRedirect(helper.init_client())

	request.set_destination('PageURIRedirectTest_1')
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('page')
	request.set_status(301)

	for u in page_b_uris:
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIRedirect)

	page_b_check = helper.get_page_uris('PageURIRedirectTest_2')

	assert page_b_check is not None
	assert len(page_b_check) == 1


def test_price_group_business_account_list_load_query():
	"""
	Tests the PriceGroupBusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupBusinessAccountList_Load_Query.xml')

	price_group_business_account_list_load_query_test_list_load()


def price_group_business_account_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupBusinessAccountListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupBusinessAccountListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('title', 'PriceGroupBusinessAccountListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupBusinessAccountListLoadQuery)

	assert len(response.get_price_group_business_accounts()) == 3


def test_price_group_business_account_update_assigned():
	"""
	Tests the PriceGroupBusinessAccount_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupBusinessAccount_Update_Assigned.xml')

	price_group_business_account_update_assigned_test_assignment()
	price_group_business_account_update_assigned_test_unassignment()


def price_group_business_account_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupBusinessAccountUpdateAssignedTest_1')
	request.set_business_account_title('PriceGroupBusinessAccountUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupBusinessAccountUpdateAssigned)

	check = helper.get_price_group_business_accounts('PriceGroupBusinessAccountUpdateAssignedTest_1', 'PriceGroupBusinessAccountUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_business_account_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupBusinessAccountUpdateAssignedTest_1')
	request.set_business_account_title('PriceGroupBusinessAccountUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupBusinessAccountUpdateAssigned)

	check = helper.get_price_group_business_accounts('PriceGroupBusinessAccountUpdateAssignedTest_1', 'PriceGroupBusinessAccountUpdateAssignedTest_2', False, True)

	assert len(check) == 1


def test_price_group_category_list_load_query():
	"""
	Tests the PriceGroupCategoryList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupCategoryList_Load_Query.xml')

	price_group_category_list_load_query_test_list_load()


def price_group_category_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupCategoryListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupCategoryListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupCategoryListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCategoryListLoadQuery)

	assert len(response.get_price_group_categories()) == 3


def test_price_group_category_update_assigned():
	"""
	Tests the PriceGroupCategory_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupCategory_Update_Assigned.xml')

	price_group_category_update_assigned_test_assignment()
	price_group_category_update_assigned_test_unassignment()


def price_group_category_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupCategoryUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCategoryUpdateAssigned)

	check = helper.get_price_group_categories('PriceGroupCategoryUpdateAssignedTest_1', 'PriceGroupCategoryUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_category_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupCategoryUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCategoryUpdateAssigned)

	check = helper.get_price_group_categories('PriceGroupCategoryUpdateAssignedTest_1', 'PriceGroupCategoryUpdateAssignedTest_2', False, True)

	assert len(check) == 1


def test_price_group_excluded_category_list_load_query():
	"""
	Tests the PriceGroupExcludedCategoryList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupExcludedCategoryList_Load_Query.xml')

	price_group_excluded_category_list_load_query_test_list_load()


def price_group_excluded_category_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupExcludedCategoryListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupExcludedCategoryListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryListLoadQuery)

	assert len(response.get_price_group_categories()) == 3


def test_price_group_excluded_category_update_assigned():
	"""
	Tests the PriceGroupExcludedCategory_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupExcludedCategory_Update_Assigned.xml')

	price_group_excluded_category_update_assigned_test_assignment()
	price_group_excluded_category_update_assigned_test_unassignment()


def price_group_excluded_category_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupExcludedCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned)

	check = helper.get_price_group_excluded_categories('PriceGroupExcludedCategoryUpdateAssignedTest_1', 'PriceGroupExcludedCategoryUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_excluded_category_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupExcludedCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupExcludedCategoryUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned)

	check = helper.get_price_group_excluded_categories('PriceGroupExcludedCategoryUpdateAssignedTest_1', 'PriceGroupExcludedCategoryUpdateAssignedTest_2', False, True)

	assert len(check) == 1


def test_price_group_excluded_product_list_load_query():
	"""
	Tests the PriceGroupExcludedProductList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupExcludedProductList_Load_Query.xml')

	price_group_excluded_product_list_load_query_test_list_load()


def price_group_excluded_product_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupExcludedProductListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupExcludedProductListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductListLoadQuery)

	assert len(response.get_price_group_products()) == 3


def test_price_group_excluded_product_update_assigned():
	"""
	Tests the PriceGroupExcludedProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupExcludedProduct_Update_Assigned.xml')

	price_group_excluded_product_update_assigned_test_assignment()
	price_group_excluded_product_update_assigned_test_unassignment()


def price_group_excluded_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupExcludedProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupExcludedProductUpdateAssignedTest_1', 'PriceGroupExcludedProductUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_excluded_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupExcludedProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupExcludedProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupExcludedProductUpdateAssignedTest_1', 'PriceGroupExcludedProductUpdateAssignedTest_2', False, True)

	assert len(check) == 1


def test_price_group_qualifying_product_list_load_query():
	"""
	Tests the PriceGroupQualifyingProductList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupQualifyingProductList_Load_Query.xml')

	price_group_qualifying_product_list_load_query_test_list_load()


def price_group_qualifying_product_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupQualifyingProductListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupQualifyingProductListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupQualifyingProductListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductListLoadQuery)

	assert len(response.get_price_group_products()) == 3


def test_price_group_qualifying_product_update_assigned():
	"""
	Tests the PriceGroupQualifyingProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupQualifyingProduct_Update_Assigned.xml')

	price_group_qualifying_product_update_assigned_test_assignment()
	price_group_equalifying_product_update_assigned_test_unassignment()


def price_group_qualifying_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupQualifyingProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductUpdateAssigned)

	check = helper.get_price_group_qualifying_products('PriceGroupQualifyingProductUpdateAssignedTest_1', 'PriceGroupQualifyingProductUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_equalifying_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupQualifyingProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupQualifyingProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupQualifyingProductUpdateAssignedTest_1', 'PriceGroupQualifyingProductUpdateAssignedTest_2', False, True)

	assert len(check) == 1


def test_price_group_delete():
	"""
	Tests the PriceGroup_Delete API Call
	"""

	helper.provision_store('PriceGroup_Delete.xml')

	price_group_delete_test_deletion()


def price_group_delete_test_deletion():
	pricegroup = helper.get_price_group('PriceGroupDeleteTest_1')

	assert pricegroup is not None

	request = merchantapi.request.PriceGroupDelete(helper.init_client(), pricegroup)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupDelete)

	check = helper.get_price_group(pricegroup.get_name())

	assert check is None


def test_price_group_insert():
	"""
	Tests the PriceGroup_Insert API Call
	"""

	helper.provision_store('PriceGroup_Insert.xml')

	price_group_insert_test_insertion()


def price_group_insert_test_insertion():
	assert helper.get_price_group('PriceGroupInsertTest_1') is None

	request = merchantapi.request.PriceGroupInsert(helper.init_client())

	request.set_name("PriceGroupInsertTest_1")
	request.set_customer_scope(merchantapi.model.PriceGroup.ELIGIBILITY_ALL)
	request.set_rate(merchantapi.model.PriceGroup.DISCOUNT_TYPE_RETAIL)
	request.set_discount(1.00)
	request.set_markup(1.00)
	request.set_module_code('discount_basket')
	request.set_exclusion(True)
	request.set_description("PriceGroupInsertTest_1")
	request.set_display(False)
	request.set_date_time_start(100)
	request.set_date_time_end(120)
	request.set_qualifying_min_subtotal(2.00)
	request.set_qualifying_max_subtotal(3.00)
	request.set_qualifying_min_quantity(4)
	request.set_qualifying_max_quantity(5)
	request.set_qualifying_min_weight(6.00)
	request.set_qualifying_max_weight(7.00)
	request.set_basket_min_subtotal(8.00)
	request.set_basket_max_subtotal(9.00)
	request.set_basket_min_quantity(10)
	request.set_basket_max_quantity(11)
	request.set_basket_min_weight(12.00)
	request.set_basket_max_weight(13.00)
	request.set_priority(2)
	request.set_module_field('Basket_Discount', 1.00)
	request.set_module_field('Basket_MaxDiscount', 1.00)
	request.set_module_field('Basket_Type', 'fixed')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupInsert)

	assert isinstance(response.get_price_group(), merchantapi.model.PriceGroup)
	assert response.get_price_group().get_discount() == 0.00
	assert response.get_price_group().get_markup() == 0.00
	assert response.get_price_group().get_exclusion() == False
	assert response.get_price_group().get_name() == 'PriceGroupInsertTest_1'
	assert response.get_price_group().get_description() == 'PriceGroupInsertTest_1'
	assert response.get_price_group().get_display() == False
	assert response.get_price_group().get_minimum_subtotal() == 2.00
	assert response.get_price_group().get_maximum_subtotal() == 3.00
	assert response.get_price_group().get_minimum_quantity() == 4.00
	assert response.get_price_group().get_maximum_quantity() == 5.00
	assert response.get_price_group().get_minimum_weight() == 6.00
	assert response.get_price_group().get_maximum_weight() == 7.00
	assert response.get_price_group().get_basket_minimum_subtotal() == 8.00
	assert response.get_price_group().get_basket_maximum_subtotal() == 9.00
	assert response.get_price_group().get_basket_minimum_quantity() == 10.00
	assert response.get_price_group().get_basket_maximum_quantity() == 11.00
	assert response.get_price_group().get_basket_minimum_weight() == 12.00
	assert response.get_price_group().get_basket_maximum_weight() == 13.00

	check = helper.get_price_group('PriceGroupInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_price_group().get_id()


def test_price_group_update():
	"""
	Tests the PriceGroup_Update API Call
	"""

	helper.provision_store('PriceGroup_Update.xml')

	price_group_update_test_update()


def price_group_update_test_update():
	pricegroup = helper.get_price_group('PriceGroupUpdateTest_1')

	assert pricegroup is not None

	request = merchantapi.request.PriceGroupUpdate(helper.init_client(), pricegroup)

	request.set_name('PriceGroupUpdateTest_1_Modified')
	request.set_description('PriceGroupUpdateTest_1_Modified')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupUpdate)

	checkA = helper.get_price_group('PriceGroupUpdateTest_1')
	checkB = helper.get_price_group('PriceGroupUpdateTest_1_Modified')

	assert checkA is None
	assert checkB is not None
	assert checkB.get_description() == 'PriceGroupUpdateTest_1_Modified'


def test_product_image_update_type():
	"""
	Tests the ProductImage_Update_Type API Call
	"""

	helper.provision_store('ProductImage_Update_Type_Clear.xml')
	helper.upload_image('graphics/ProductImageUpdateTypeTest.jpg')
	helper.provision_store('ProductImage_Update_Type.xml')

	product_image_update_type_test_update()


def product_image_update_type_test_update():
	product = helper.get_product('ProductImageUpdateTypeTest')

	assert product is not None
	assert len(product.get_product_image_data()) == 1

	image_types_request = merchantapi.request.ImageTypeListLoadQuery(helper.init_client())
	image_types_request.set_filters(image_types_request.filter_expression().equal('code', 'ProductImageUpdateTypeTestB'))

	image_types_response = image_types_request.send()

	assert len(image_types_response.get_image_types()) == 1

	request = merchantapi.request.ProductImageUpdateType(helper.init_client())

	request.set_product_image_id(product.get_product_image_data()[0].get_id())
	request.set_image_type_id(image_types_response.get_image_types()[0].get_id())

	response = request.send()

	check = helper.get_product('ProductImageUpdateTypeTest')

	assert check is not None
	assert len(check.get_product_image_data()) == 1
	assert check.get_product_image_data()[0].get_type_id() == image_types_response.get_image_types()[0].get_id()


def test_product_uri_insert():
	"""
	Tests the ProductURI_Insert API Call
	"""

	helper.provision_store('ProductURI_Insert.xml')

	product_uri_insert_test_insertion()


def product_uri_insert_test_insertion():
	test_uri = '/ProductURIInsertTest_1_1'
	product = helper.get_product('ProductURIInsertTest_1')

	assert product is not None

	request = merchantapi.request.ProductURIInsert(helper.init_client(), product)

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_product('ProductURIInsertTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_product_uri_update():
	"""
	Tests the ProductURI_Update API Call
	"""

	helper.provision_store('ProductURI_Update.xml')

	product_uri_update_test_update()


def product_uri_update_test_update():
	product = helper.get_product('ProductURIUpdateTest_1')

	assert product is not None
	assert len(product.get_uris()) == 2

	uri = None

	for u in product.get_uris():
		if u.get_canonical():
			continue
		uri = u
		break

	assert uri is not None

	test_uri = uri.get_uri() + '_1_1'

	request = merchantapi.request.ProductURIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIUpdate)

	check = helper.get_product('ProductURIUpdateTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None


def test_product_uri_list_load_query():
	"""
	Tests the ProductURIList_Load_Query API Call
	"""

	helper.provision_store('ProductURIList_Load_Query.xml')

	product_uri_list_load_query_test_list_load()


def product_uri_list_load_query_test_list_load():
	product = helper.get_product('ProductURIListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductURIListLoadQuery(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIListLoadQuery)

	assert len(response.get_uris()) > 1

	for uri in response.get_uris():
		assert uri.get_product_id() == product.get_id()
		if not uri.get_canonical():
			assert 'ProductURIListLoadQueryTest' in uri.get_uri()


def test_product_uri_list_delete():
	"""
	Tests the ProductURIList_Delete API Call
	"""

	helper.provision_store('ProductURIList_Delete.xml')

	product_uri_list_delete_test_deletion()


def product_uri_list_delete_test_deletion():
	product = helper.get_product('ProductURIListDeleteTest_1')

	assert product is not None
	assert len(product.get_uris()) > 1

	request = merchantapi.request.ProductURIListDelete(helper.init_client())

	for u in product.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIListDelete)

	check = helper.get_product('ProductURIListDeleteTest_1')

	assert check is not None
	assert len(check.get_uris()) == 1


def test_product_uri_redirect():
	"""
	Tests the ProductURI_Redirect API Call
	"""

	helper.provision_store('ProductURI_Redirect.xml')

	product_uri_redirect_test_redirect()


def product_uri_redirect_test_redirect():
	product_a = helper.get_product('ProductURIRedirectTest_1')
	product_b = helper.get_product('ProductURIRedirectTest_2')

	assert product_a is not None
	assert product_b is not None
	assert len(product_a.get_uris()) == 3
	assert len(product_b.get_uris()) == 3

	request = merchantapi.request.ProductURIRedirect(helper.init_client())

	request.set_destination(product_a.get_code())
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('product')
	request.set_status(301)

	for u in product_b.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIRedirect)

	product_b_check = helper.get_product('ProductURIRedirectTest_2')

	assert product_b_check is not None
	assert len(product_b_check.get_uris()) == 1


def test_product_variant_list_load_query():
	"""
	Tests the ProductVariantList_Load_Query API Call
	"""

	helper.provision_store('ProductVariantList_Load_Query.xml')

	product_variant_list_load_query_test_list_load()


def product_variant_list_load_query_test_list_load():
	product = helper.get_product('ProductVariantListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductVariantListLoadQuery(helper.init_client())

	request.set_product_code(product.get_code())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListLoadQuery)

	assert len(response.get_product_variants()) > 0

	for v in response.get_product_variants():
		assert product.get_id() == v.get_product_id()


def test_product_variant_list_delete():
	"""
	Tests the ProductVariantList_Delete API Call
	"""

	helper.provision_store('ProductVariantList_Delete.xml')

	product_variant_list_delete_test_deletion()


def product_variant_list_delete_test_deletion():
	product = helper.get_product('ProductVariantListDeleteTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) > 0

	request = merchantapi.request.ProductVariantListDelete(helper.init_client())

	request.set_product_code(product.get_code())

	for v in variants:
		request.add_product_variant(v)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListDelete)

	check_variants = helper.get_product_variants(product.get_code())

	for v in variants:
		for cv in check_variants:
			assert cv.get_variant_id() != v.get_variant_id()


def test_product_variant_insert():
	"""
	Tests the ProductVariant_Insert API Call
	"""

	helper.provision_store('ProductVariant_Insert.xml')

	product_variant_insert_test_insertion()
	product_variant_insert_test_insertion_by_codes()


def product_variant_insert_test_insertion():
	product = helper.get_product('ProductVariantInsertTest_1')
	part_a = helper.get_product('ProductVariantInsertTest_1_1')
	part_b = helper.get_product('ProductVariantInsertTest_1_2')

	assert product is not None
	assert part_a is not None
	assert part_b is not None

	request = merchantapi.request.ProductVariantInsert(helper.init_client(), product)

	attr = merchantapi.model.VariantAttribute()

	attr.set_attribute_id(product.get_attributes()[0].get_id())
	attr.set_attribute_template_attribute_id(0)
	attr.set_option_id(product.get_attributes()[0].get_options()[0].get_id())

	request.add_variant_attribute(attr)

	part_1 = merchantapi.model.VariantPart()
	part_2 = merchantapi.model.VariantPart()

	part_1.set_part_id(part_a.get_id())
	part_1.set_quantity(1)

	part_2.set_part_id(part_b.get_id())
	part_2.set_quantity(1)

	request.add_variant_part(part_1)
	request.add_variant_part(part_2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantInsert)

	assert response.get_product_variant().get_product_id() == product.get_id()
	assert response.get_product_variant().get_variant_id() > 0


def product_variant_insert_test_insertion_by_codes():
	product = helper.get_product('ProductVariantInsertTest_1')
	part_a = helper.get_product('ProductVariantInsertTest_1_1')
	part_b = helper.get_product('ProductVariantInsertTest_1_2')

	assert product is not None
	assert part_a is not None
	assert part_b is not None

	request = merchantapi.request.ProductVariantInsert(helper.init_client(), product)

	attr = merchantapi.model.VariantAttribute()

	attr.set_attribute_code(product.get_attributes()[0].get_code())
	attr.set_option_code(product.get_attributes()[0].get_options()[0].get_code())

	request.add_variant_attribute(attr)

	part_1 = merchantapi.model.VariantPart()
	part_2 = merchantapi.model.VariantPart()

	part_1.set_part_code(part_a.get_code())
	part_1.set_quantity(1)

	part_2.set_part_code(part_b.get_code())
	part_2.set_quantity(1)

	request.add_variant_part(part_1)
	request.add_variant_part(part_2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantInsert)

	assert response.get_product_variant().get_product_id() == product.get_id()
	assert response.get_product_variant().get_variant_id() > 0


def test_product_variant_update():
	"""
	Tests the ProductVariant_Update API Call
	"""

	helper.provision_store('ProductVariant_Update.xml')

	product_variant_update_test_update()


def product_variant_update_test_update():
	product = helper.get_product('ProductVariantUpdateTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) > 0

	for variant in variants:
		assert len(variant.get_parts()) > 0

		request = merchantapi.request.ProductVariantUpdate(helper.init_client())

		request.set_product_code(product.get_code())
		request.set_variant_id(variant.get_variant_id())

		for part in variant.get_parts():
			assert part.get_quantity() == 2

			variant_part = merchantapi.model.VariantPart()

			variant_part.set_part_id(part.get_product_id())
			variant_part.set_quantity(3)

			request.add_variant_part(variant_part)

		for dimension in variant.get_dimensions():
			variant_attr = merchantapi.model.VariantAttribute()
			variant_attr.set_attribute_id(dimension.get_attribute_id())
			variant_attr.set_option_id(dimension.get_option_id())

			request.add_variant_attribute(variant_attr)

		response = request.send()

		helper.validate_response_success(response, merchantapi.response.ProductVariantUpdate)

	for v in helper.get_product_variants(product.get_code()):
		for p in v.get_parts():
			assert p.get_quantity() ==3


def test_product_variant_generate():
	"""
	Tests the ProductVariant_Generate API Call
	"""

	helper.provision_store('ProductVariant_Generate.xml')

	product_variant_generate_test_generation()


def product_variant_generate_test_generation():
	product = helper.get_product('ProductVariantGenerateTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) == 0

	request = merchantapi.request.ProductVariantGenerate(helper.init_client())
	request.set_product_code(product.get_code())
	request.set_pricing_method(request.VARIANT_PRICING_METHOD_MASTER);

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantGenerate)

	check_variants = helper.get_product_variants(product.get_code())

	assert len(check_variants) > 0


def test_product_variant_generate_delimiter():
	"""
	Tests the ProductVariant_Generate_Delimiter API Call
	"""

	helper.provision_store('ProductVariant_Generate_Delimiter.xml')

	product_variant_generate_delimiter_test_generation()


def product_variant_generate_delimiter_test_generation():
	product = helper.get_product('ProductVariantGenerateDelimiterTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) == 0

	request = merchantapi.request.ProductVariantGenerateDelimiter(helper.init_client())
	request.set_product_code(product.get_code())
	request.set_pricing_method(request.VARIANT_PRICING_METHOD_MASTER);
	request.set_delimiter('_')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantGenerateDelimiter)

	check_variants = helper.get_product_variants(product.get_code())

	assert len(check_variants) > 0


def test_product_kit_list_load_query():
	"""
	Tests the ProductKitList_Load_Query API Call
	"""

	helper.provision_store('ProductKitList_Load_Query.xml')

	product_kit_list_load_query_test_list_load()


def product_kit_list_load_query_test_list_load():
	product = helper.get_product('ProductKitListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductKitListLoadQuery(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitListLoadQuery)

	assert len(response.get_product_kits()) > 0


def test_product_kit_generate_variants():
	"""
	Tests the ProductKit_Generate_Variants API Call
	"""

	helper.provision_store('ProductKit_Generate_Variants.xml')

	product_kit_generate_variants_test_generation()


def product_kit_generate_variants_test_generation():
	product = helper.get_product('ProductKitGenerateVariantsTest_1')

	assert product is not None

	request = merchantapi.request.ProductKitGenerateVariants(helper.init_client(), product)

	request.set_pricing_method(request.VARIANT_PRICING_METHOD_MASTER)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitGenerateVariants)

	assert helper.get_product_kit_variant_count(product.get_code()) == 4


def test_product_kit_update_parts():
	"""
	Tests the ProductKit_Update_Parts API Call
	"""

	helper.provision_store('ProductKit_Update_Parts.xml')

	product_kit_update_parts_test_update()


def product_kit_update_parts_test_update():
	product = helper.get_product('ProductKitUpdatePartsTest_1')

	assert product is not None
	assert len(product.get_attributes()) == 2

	p = 0
	for a in product.get_attributes():
		for o in a.get_options():
			p = p + 1
			part_product = helper.get_product('ProductKitUpdatePartsTest_1_%d' % p)

			assert part_product is not None

			request = merchantapi.request.ProductKitUpdateParts(helper.init_client(), product)

			request.set_attribute_id(a.get_id())
			request.set_option_id(o.get_id())

			part = merchantapi.model.KitPart()

			part.set_part_id(part_product.get_id())
			part.set_quantity(1)

			request.add_kit_part(part)

			response = request.send()

			helper.validate_response_success(response, merchantapi.response.ProductKitUpdateParts)

	assert p > 0


def test_product_kit_variant_count():
	"""
	Tests the ProductKit_Variant_Count API Call
	"""

	helper.provision_store('ProductKit_Variant_Count.xml')

	product_kit_variant_count_test_count()


def product_kit_variant_count_test_count():
	product = helper.get_product('ProductKitVariantCountTest_1')

	request = merchantapi.request.ProductKitVariantCount(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitVariantCount)

	assert response.get_variants() == 4


def test_related_product_list_load_query():
	"""
	Tests the RelatedProductList_Load_Query API Call
	"""

	helper.provision_store('RelatedProductList_Load_Query.xml')

	related_product_list_load_query_test_list_load()


def related_product_list_load_query_test_list_load():
	product = helper.get_product('RelatedProductListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.RelatedProductListLoadQuery(helper.init_client(), product)

	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductListLoadQuery)

	assert len(response.get_related_products()) == 5

	for r in response.get_related_products():
		assert 'RelatedProductListLoadQueryTest_1' in r.get_code()


def test_related_product_update_assigned():
	"""
	Tests the RelatedProduct_Update_Assigned API Call
	"""

	helper.provision_store('RelatedProduct_Update_Assigned.xml')

	related_product_update_assigned_test_assignment()
	related_product_update_assigned_test_unassignment()


def related_product_update_assigned_test_assignment():
	product = helper.get_product('RelatedProductUpdateAssignedTest_1')

	assert product is not None

	related = helper.get_related_products(product.get_code(), '', True, False)
	to_assign = helper.get_product(product.get_code() + '_1')

	assert len(related) >= 0
	assert to_assign is not None

	for r in related:
		assert r.get_id() != to_assign.get_id()

	request = merchantapi.request.RelatedProductUpdateAssigned(helper.init_client(), product)

	request.set_related_product_id(to_assign.get_id())
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductUpdateAssigned)

	check_related = helper.get_related_products(product.get_code(), to_assign.get_code(), True, False)

	assert len(check_related) == 1


def related_product_update_assigned_test_unassignment():

	product = helper.get_product('RelatedProductUpdateAssignedTest_1')

	assert product is not None

	related = helper.get_related_products(product.get_code(), product.get_code() + '_2', True, False)
	to_unassign = helper.get_product(product.get_code() + '_2')

	assert len(related) == 1
	assert to_unassign is not None

	request = merchantapi.request.RelatedProductUpdateAssigned(helper.init_client(), product)

	request.set_related_product_id(to_unassign.get_id())
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductUpdateAssigned)

	check_related = helper.get_related_products(product.get_code(), to_unassign.get_code(), False, True)

	assert len(check_related) == 1


def test_store_load():
	"""
	Tests the Store_Load API Call
	"""

	store_load_test_load()


def store_load_test_load():
	request = merchantapi.request.StoreLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreLoad)

	assert isinstance(response.get_store(), merchantapi.model.Store)


def test_store_list_load_query():
	"""
	Tests the StoreList_Load_Query API Call
	"""

	store_list_load_query_test_load()


def store_list_load_query_test_load():
	request = merchantapi.request.StoreLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreLoad)

	assert isinstance(response.get_store(), merchantapi.model.Store)


def test_uri_list_load_query():
	"""
	Tests the URIList_Load_Query API Call
	"""

	helper.provision_store('URIList_Load_Query.xml')

	uri_list_load_query_test_list_load()


def uri_list_load_query_test_list_load():
	request = merchantapi.request.StoreListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreListLoadQuery)

	assert len(response.get_stores()) > 0


def test_uri_insert():
	"""
	Tests the URI_Insert API Call
	"""

	helper.provision_store('URI_Insert.xml')

	uri_insert_test_insertion_product()
	uri_insert_test_insertion_category()
	uri_insert_test_insertion_feed()
	uri_insert_test_insertion_page()


def uri_insert_test_insertion_product():
	test_uri = '/uri-insert-product-test-api'

	product = helper.get_product('UriInsertTest')

	for uri in product.get_uris():
		assert uri.get_uri() != test_uri

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(product.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PRODUCT)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri


def uri_insert_test_insertion_category():
	test_uri = '/uri-insert-category-test-api'

	category = helper.get_category('UriInsertTest')

	for uri in category.get_uris():
		assert uri.get_uri() != test_uri

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(category.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_CATEGORY)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri


def uri_insert_test_insertion_feed():
	test_uri = '/uri-insert-feed-test-api'

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriInsertTest_1')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_FEED)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_uri(test_uri)

	assert check is not None
	assert check.get_feed_id() > 0


def uri_insert_test_insertion_page():
	test_uri = '/uri-insert-page-test-api'

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriInsertTest_2')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PAGE)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_uri(test_uri)

	assert check is not None
	assert check.get_page_id() > 0


def test_uri_update():
	"""
	Tests the URI_Update API Call
	"""

	helper.provision_store('URI_Update.xml')

	uri_update_test_update_product()
	uri_update_test_update_category()
	uri_update_test_update_feed()
	uri_update_test_update_page()


def uri_update_test_update_product():
	test_uri = '/uri-update-product-test-api'

	product = helper.get_product('UriUpdateTest')

	assert len(product.get_uris()) == 1

	uri = product.get_uris()[0]

	request = merchantapi.request.URIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(product.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PRODUCT)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = None
	for u in helper.get_product(product.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u

	assert check_uri is not None


def uri_update_test_update_category():
	test_uri = '/uri-update-category-test-api'

	category = helper.get_category('UriUpdateTest')

	assert len(category.get_uris()) == 1

	uri = category.get_uris()[0]

	request = merchantapi.request.URIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(category.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_CATEGORY)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = None
	for u in helper.get_category(category.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u

	assert check_uri is not None



def uri_update_test_update_feed():
	test_uri = '/uri-update-feed-test-api'

	uris = helper.get_feed_uris('UriUpdateTest_1')

	assert len(uris) > 0

	request = merchantapi.request.URIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriUpdateTest_1')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_FEED)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = helper.get_uri(test_uri)

	assert check_uri is not None
	assert check_uri.get_id() == uris[0].get_id()



def uri_update_test_update_page():
	test_uri = '/uri-update-page-test-api'

	uris = helper.get_page_uris('UriUpdateTest_2')

	assert len(uris) > 0

	request = merchantapi.request.URIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriUpdateTest_2')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PAGE)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = helper.get_uri(test_uri)

	assert check_uri is not None
	assert check_uri.get_id() == uris[0].get_id()



def test_uri_delete():
	"""
	Tests the URI_Delete API Call
	"""

	helper.provision_store('URI_Delete.xml')

	uri_delete_test_deletion()



def uri_delete_test_deletion():
	product = helper.get_product('URIDeleteTest_1')

	assert product is not None
	assert len(product.get_uris()) > 1

	uri = None

	for u in product.get_uris():
		if u.get_canonical():
			uri = u
			break

	assert uri is not None

	request = merchantapi.request.URIDelete(helper.init_client(), uri)
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIDelete)

	check_uri = None
	for u in helper.get_product(product.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u
			break

	assert check_uri is None


def test_uri_list_delete():
	"""
	Tests the URIList_Delete API Call
	"""

	helper.provision_store('URIList_Delete.xml')

	uri_list_delete_test_deletion()


def uri_list_delete_test_deletion():
	product = helper.get_product('URIListDeleteTest_1')

	assert product is not None
	assert len(product.get_uris()) > 1

	request = merchantapi.request.URIListDelete(helper.init_client())
	
	for u in product.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIListDelete)

	assert len(helper.get_product(product.get_code()).get_uris()) == 1


def test_product_attribute_and_option_list_load_query():
	"""
	Tests the ProductAttributeAndOptionList_Load_Query API Call
	"""

	helper.provision_store('ProductAttributeAndOptionList_Load_Query.xml')

	product_attribute_and_option_list_load_query_test_list_load()


def product_attribute_and_option_list_load_query_test_list_load():
	request = merchantapi.request.ProductAttributeAndOptionListLoadQuery(helper.init_client())

	request.set_product_code('PATLLQ')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductAttributeAndOptionListLoadQuery)

	assert len(response.get_attributes()) == 2
	assert response.get_attributes()[0].get_product_id() > 0
	assert 'PATLLQ' in response.get_attributes()[0].get_code()
	assert response.get_attributes()[0].get_type() == 'template'
	assert isinstance(response.get_attributes()[0].get_template(), merchantapi.model.ProductAttributeListTemplate)
	assert response.get_attributes()[0].get_template().get_id() > 0

	assert response.get_attributes()[1].get_product_id() > 0
	assert 'PATLLQ' in response.get_attributes()[1].get_code()
	assert response.get_attributes()[1].get_type() == 'checkbox'


def test_attribute_copy_linked_template():
	"""
	Tests the Attribute_CopyLinkedTemplate API Call
	"""

	helper.provision_store('Attribute_CopyLinkedTemplate.xml')

	attribute_copy_linked_template_test_copy()


def attribute_copy_linked_template_test_copy():
	request = merchantapi.request.AttributeCopyLinkedTemplate(helper.init_client())

	request.set_product_code('AttributeCopyLinkedTemplate')
	request.set_attribute_code('AttributeCopyLinkedTemplate')

	response = request.send()

	check = helper.get_attribute_template('AttributeCopyLinkedTemplate')

	assert check != None


def test_attribute_copy_template():
	"""
	Tests the Attribute_CopyTemplate API Call
	"""

	helper.provision_store('Attribute_CopyTemplate.xml')

	attribute_copy_template_test_copy()


def attribute_copy_template_test_copy():
	check = helper.get_product('AttributeCopyTemplate')
	
	assert check is not None
	assert len(check.get_attributes()) == 0

	request = merchantapi.request.AttributeCopyTemplate(helper.init_client())

	request.set_product_code('AttributeCopyTemplate')
	request.set_attribute_template_code('AttributeCopyTemplate')

	response = request.send()

	check = helper.get_attribute_template('AttributeCopyTemplate')

	assert check is not None
	assert check.get_code() == 'AttributeCopyTemplate'


def test_customer_subscription_list_load_query():
	"""
	Tests the CustomerSubscriptionList_Load_Query API Call
	"""

	helper.provision_store('CustomerSubscriptionList_Load_Query.xml')

	customer_subscription_list_load_query_test_list_load()
	customer_subscription_list_load_query_test_list_load_with_filters()


def customer_subscription_list_load_query_test_list_load():
	customer = helper.get_customer('CSLLQ_1')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_1')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ')

	assert methods is not None and len(methods) == 1

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 2

	for sub in response.get_customer_subscriptions():
		assert sub.get_id() == sub1.get_id() or sub.get_id() == sub2.get_id()


def customer_subscription_list_load_query_test_list_load_with_filters():
	customer = helper.get_customer('CSLLQ_2')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_2')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ');

	assert methods is not None and len(methods) == 1

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())
	request.filters.equal('product_code', products[1].get_code())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 1
	assert response.get_customer_subscriptions()[0].get_id() == sub2.get_id()


def test_product_and_subscription_term_list_load_query():
	"""
	Tests the ProductAndSubscriptionTermList_Load_Query API Call
	"""

	helper.provision_store('ProductAndSubscriptionTermList_Load_Query.xml')

	product_and_subscription_term_list_load_query_test_list_load()


def product_and_subscription_term_list_load_query_test_list_load():
	codes = [ 'PASTLLQ_1', 'PASTLLQ_2' ]
	terms = [ 'daily', 'monthly' ]

	request = merchantapi.request.ProductAndSubscriptionTermListLoadQuery(helper.init_client())

	request.filters.is_in('code', ','.join(codes))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductAndSubscriptionTermListLoadQuery)

	assert len(response.get_product_and_subscription_terms()) is 3
	for term in response.get_product_and_subscription_terms():
		assert term.get_code() in codes
		assert term.get_term_frequency() in  terms


def test_product_subscription_term_list_load_query():
	"""
	Tests the ProductSubscriptionTermList_Load_Query API Call
	"""

	helper.provision_store('ProductSubscriptionTermList_Load_Query.xml')

	product_subscription_term_list_load_query_test_list_load()


def product_subscription_term_list_load_query_test_list_load():
	terms = [ 'daily', 'weekly', 'monthly' ]
	descriptions = [ 'Daily', 'Weekly', 'Monthly' ]

	request = merchantapi.request.ProductSubscriptionTermListLoadQuery(helper.init_client())

	request.set_product_code('PSTLLQ_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductSubscriptionTermListLoadQuery)

	assert len(response.get_product_subscription_terms()) is 3
	for term in response.get_product_subscription_terms():
		assert term.get_frequency() in terms
		assert term.get_description() in  descriptions


def test_subscription_shipping_method_list_load_query():
	"""
	Tests the SubscriptionShippingMethodList_Load_Query API Call
	"""

	helper.provision_store('SubscriptionShippingMethodList_Load_Query.xml')

	subscription_shipping_method_list_load_query_test_list_load()


def subscription_shipping_method_list_load_query_test_list_load():
	customer = helper.get_customer('SSMLLQ_1')
	product = helper.get_product('SSMLLQ_1')

	assert customer is not None
	assert product is not None

	addresses = helper.get_customer_addresses(customer.get_login())

	assert addresses is not None
	assert len(addresses) > 0

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	request = merchantapi.request.SubscriptionShippingMethodListLoadQuery(helper.init_client())

	request.set_product_id(product.get_id())
	request.set_customer_id(customer.get_id())
	request.set_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_quantity(1)
	request.set_product_subscription_term_description('Daily')

	request.filters.contains('method', 'SSMLLQ_')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionShippingMethodListLoadQuery)

	assert len(response.get_subscription_shipping_methods()) is 3
	for method in response.get_subscription_shipping_methods():
		assert method.get_module() is not None
		assert method.get_module().get_id() > 0
		assert 'SSMLLQ_' in method.get_method_name()


def test_subscription_update():
	"""
	Tests the Subscription_Update API Call
	"""

	helper.provision_store('Subscription_Update.xml')

	subscription_update_test_update()


def subscription_update_test_update():
	customer = helper.get_customer('Subscription_Update_1')
	addresses = helper.get_customer_addresses('Subscription_Update_1')
	product = helper.get_product('Subscription_Update_1')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) > 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Update')

	assert methods is not None
	assert len(methods) is 1

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('red')

	subscription = helper.create_subscription(customer, product, 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'Subscription_Update', 1, [ attr1 ])

	assert subscription is not None

	payment_card_change = helper.register_payment_card_with_address(customer, addresses[1])

	assert payment_card_change is not None

	request = merchantapi.request.SubscriptionUpdate(helper.init_client())

	request.set_subscription_id(subscription.get_id())
	request.set_payment_card_id(payment_card_change.get_id())
	request.set_quantity(1)
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))

	attr1change = merchantapi.model.SubscriptionAttribute()

	attr1change.set_code('color')
	attr1change.set_value('green')

	request.add_attribute(attr1change)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionUpdate)

	check = helper.get_subscription(customer.get_id(), subscription.get_id())

	assert check is not None

	assert check.get_customer_payment_card_id() == payment_card_change.get_id()
	assert len(check.get_options()) is 1
	assert check.get_options()[0].get_value() == 'green'


def test_subscription_insert():
	"""
	Tests the Subscription_Insert API Call
	"""

	helper.provision_store('Subscription_Insert.xml')

	subscription_insert_test_insert()
	subscription_insert_test_insert_with_attribute()


def subscription_insert_test_insert():
	customer = helper.get_customer('Subscription_Insert_1')
	addresses = helper.get_customer_addresses('Subscription_Insert_1')
	product = helper.get_product('Subscription_Insert_1')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Insert')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionInsert(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('Subscription_Insert')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionInsert)

	assert response.get_subscription() is not None
	assert response.get_subscription().get_id() > 0


def subscription_insert_test_insert_with_attribute():
	customer = helper.get_customer('Subscription_Insert_2')
	addresses = helper.get_customer_addresses('Subscription_Insert_2')
	product = helper.get_product('Subscription_Insert_2')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Insert')

	assert methods is not None
	assert len(methods) is 1

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('green')

	request = merchantapi.request.SubscriptionInsert(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('Subscription_Insert')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.add_attribute(attr1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionInsert)

	assert response.get_subscription() is not None
	assert response.get_subscription().get_id() > 0
	assert len(response.get_subscription().get_options()) == 1
	assert response.get_subscription().get_options()[0].get_value() == "green"


def test_subscription_list_delete():
	"""
	Tests the SubscriptionList_Delete API Call
	"""

	helper.provision_store('SubscriptionList_Delete.xml')

	subscription_list_delete_test_deletion()


def subscription_list_delete_test_deletion():
	customer = helper.get_customer('SubscriptionList_Delete_1')
	addresses = helper.get_customer_addresses('SubscriptionList_Delete_1')
	products = helper.get_products(['SubscriptionList_Delete_1', 'SubscriptionList_Delete_2', 'SubscriptionList_Delete_3'])

	assert customer is not None
	assert products is not None
	assert len(products) == 3
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionList_Delete')

	assert methods is not None
	assert len(methods) is 1

	subscription1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])
	subscription2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])
	subscription3 = helper.create_subscription(customer, products[2], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])

	assert subscription1 is not None
	assert subscription2 is not None
	assert subscription3 is not None

	request = merchantapi.request.SubscriptionListDelete(helper.init_client())

	request.add_subscription(subscription1)
	request.add_subscription(subscription2)
	request.add_subscription(subscription3)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionListDelete)

	check_request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())
	check_request.set_customer_id(customer.get_id())
	check_request.filters.is_in('id', ','.join([str(subscription1.get_id()), str(subscription2.get_id()), str(subscription3.get_id())]))

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(check_response.get_customer_subscriptions()) == 0


def test_subscription_and_order_item_add():
	"""
	Tests the SubscriptionAndOrderItem_Add API Call
	"""

	helper.provision_store('SubscriptionAndOrderItem_Add.xml')

	subscription_and_order_item_add_test_add()
	subscription_and_order_item_add_test_add_with_attribute()


def subscription_and_order_item_add_test_add():
	customer = helper.get_customer('SubscriptionAndOrderItem_Add_1')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Add_1')
	product = helper.get_product('SubscriptionAndOrderItem_Add_1')
	order = helper.get_order(678568)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Add')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('SubscriptionAndOrderItem_Add')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.set_order_id(order.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_subscription_id() > 0

	check = helper.get_order(order.get_id())

	assert check is not None
	assert check.get_items()[0].get_subscription_id() > 0


def subscription_and_order_item_add_test_add_with_attribute():
	customer = helper.get_customer('SubscriptionAndOrderItem_Add_2')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Add_2')
	product = helper.get_product('SubscriptionAndOrderItem_Add_2')
	order = helper.get_order(678569)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Add')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('SubscriptionAndOrderItem_Add')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.set_order_id(order.get_id())

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('green')

	request.add_attribute(attr1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_subscription_id() > 0

	check = helper.get_order(order.get_id())

	assert check is not None
	assert check.get_items()[0].get_subscription_id() > 0
	assert check.get_items()[0].get_subscription().get_options()[0].get_value() == 'green'


def test_subscription_and_order_item_update():
	"""
	Tests the SubscriptionAndOrderItem_Update API Call
	"""

	helper.provision_store('SubscriptionAndOrderItem_Update.xml')

	subscription_and_order_item_update_test_update()


def subscription_and_order_item_update_test_update():
	customer = helper.get_customer('SubscriptionAndOrderItem_Update_1')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Update_1')
	product = helper.get_product('SubscriptionAndOrderItem_Update_1')
	order = helper.get_order(678568)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Update')

	assert methods is not None
	assert len(methods) is 1

	create_request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	create_request.set_product_code(product.get_code())
	create_request.set_customer_id(customer.get_id())
	create_request.set_customer_address_id(addresses[0].get_id())
	create_request.set_payment_card_id(payment_card.get_id())
	create_request.set_product_subscription_term_description('Daily')
	create_request.set_ship_id(methods[0].get_module().get_id())
	create_request.set_ship_data('SubscriptionAndOrderItem_Add')
	create_request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	create_request.set_quantity(1)
	create_request.set_order_id(order.get_id())

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('red')

	create_request.add_attribute(attr1)

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.SubscriptionAndOrderItemAdd)

	load = helper.get_order(order.get_id())

	assert load is not None
	assert load.get_items()[0].get_subscription_id() > 0

	payment_card_change = helper.register_payment_card_with_address(customer, addresses[1])

	assert payment_card_change is not None

	request = merchantapi.request.SubscriptionAndOrderItemUpdate(helper.init_client())

	request.set_order_id(load.get_id());
	request.set_line_id(load.get_items()[0].get_line_id())
	request.set_subscription_id(load.get_items()[0].get_subscription_id())
	request.set_payment_card_id(payment_card_change.get_id())
	request.set_quantity(1)
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))

	attr1change = merchantapi.model.SubscriptionAttribute()

	attr1change.set_code('color')
	attr1change.set_value('green')

	request.add_attribute(attr1change)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemUpdate)

	check = helper.get_subscription(customer.get_id(), load.get_items()[0].get_subscription_id())

	assert check is not None

	assert check.get_customer_payment_card_id() == payment_card_change.get_id()
	assert check.get_options() is not None and len(check.get_options()) == 1
	assert check.get_options()[0].get_value() == 'green'


def test_subscription_list_load_query():
	"""
	Tests the SubscriptionList_Load_Query API Call
	"""

	helper.provision_store('SubscriptionList_Load_Query.xml')

	subscription_list_load_query_test_list_load()


def subscription_list_load_query_test_list_load():
	customer = helper.get_customer('SLLQ_1')
	products = helper.get_products(['SLLQ_1', 'SLLQ_2'])
	addresses = helper.get_customer_addresses('SLLQ_1')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'SLLQ')

	assert methods is not None and len(methods) > 0

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'SLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'SLLQ', 1)

	request = merchantapi.request.SubscriptionListLoadQuery(helper.init_client())
	request.get_filters().equal('customer_login', customer.get_login())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionListLoadQuery)

	assert len(response.get_subscriptions()) == 2

	for sub in response.get_subscriptions():
		assert sub.get_id() == sub1.get_id() or sub.get_id() == sub2.get_id()


def test_request_builder():
	"""
	Tests the RequestBuilder functionality
	"""

	helper.provision_store('ProductList_Load_Query.xml')

	test_request_builder_get_set()
	test_request_builder_function()
	test_list_query_request_builder_function()


def test_request_builder_get_set():
	request = merchantapi.request.RequestBuilder(helper.init_client(), 'Function', { 'foo': 'bar' })

	request.set_store_code('Store_Code')
	request.set('bar', 'foo')

	assert request.function == 'Function'
	assert request.store_code == 'Store_Code'
	assert request.get('foo') == 'bar'
	assert request.get('bar') == 'foo'


def test_request_builder_function():
	request = merchantapi.request.RequestBuilder(helper.init_client())

	request.set_function('ProductList_Load_Query')
	request.set('Count', 1)
	
	response = request.send()
	helper.validate_response_success(response, merchantapi.response.RequestBuilder)

	assert isinstance(response.get_data(), dict)
	assert isinstance(response.get_data()['data'], dict)
	assert isinstance(response.get_data()['data']['data'], list)
	assert len(response.get_data()['data']['data']) == 1


def test_list_query_request_builder_function():
	request = merchantapi.request.ListQueryRequestBuilder(helper.init_client())

	request.set_function('ProductList_Load_Query')
	request.set_count(1)
	
	response = request.send()
	helper.validate_response_success(response, merchantapi.response.ListQueryRequestBuilder)

	assert isinstance(response.get_data(), dict)
	assert isinstance(response.get_data()['data'], dict)
	assert isinstance(response.get_data()['data']['data'], list)
	assert len(response.get_data()['data']['data']) == 1
