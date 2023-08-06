"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/9/15 14:14
"""

from django.core.paginator import Paginator, EmptyPage

from xj_enroll.service.subitem_service import SubitemService
from ..models import Enroll, EnrollRecord
from ..utils.model_handle import format_params_handle


class EnrollServices:
    def __init__(self):
        pass

    @staticmethod
    def enroll_add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "user_id", "category_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code", "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount", "paid_amount", "unpaid_amount", "commision", "deposit",
                "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time", "create_time", "update_time", "snapshot", "remark",
            ],
        )
        try:
            instance = Enroll.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return instance.to_json(), None

    @staticmethod
    def enroll_detail(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, "不存的报名信息"
        enroll_detail = enroll_obj.first().to_json()

        # 报名记录筛选出报名用户ID
        enroll_user_ids = list(EnrollRecord.objects.filter(enroll_id=enroll_id).values("user_id"))
        enroll_detail["enroll_user_ids"] = [i["user_id"] for i in enroll_user_ids]

        # 报名分项
        enroll_detail["subitem"], err = SubitemService.list({"enroll_id": enroll_id}, False)
        # 清单总数暂时不做处理
        # enroll_detail["detailed_count"] = 0
        # if not err and enroll_detail["subitem"]:
        #     enroll_detail["detailed_count"] = enroll_detail["subitem"][0]['count']

        return enroll_detail, None

    @staticmethod
    def enroll_list(params, filter_fields=None, need_pagination=True):
        # 字段处理
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        filter_fields_list = filter_fields.split(";") if filter_fields else []
        params['enroll_status_code'] = params['enroll_status_code'].split(";") if params.get("enroll_status_code") else None
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "thread_id", "category_id", "thread_id_list", "trading_relate", "region_code", "spend_time_start", "enroll_status_code",
                "spend_time_end", "create_time_start", "create_time_end", "finish_time_start", "finish_time_end",
                "open_time_start", "open_time_end", "enroll_status_code", "has_subitem"
            ],
            alias_dict={
                "spend_time_start": "spend_time__gte", "spend_time_end": "spend_time__lte", "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "finish_time_start": "finish_time__gte", "open_time_start": "open_time__gte", "open_time_end": "open_time__lte", "enroll_classify_value": "classify__value",
                "enroll_category_value": "category__value", "enroll_status_code": "enroll_status_code__in", "thread_id_list": "thread_id__in"
            }
        )
        # 全部展示
        enroll_obj = Enroll.objects.filter(**params).values(*filter_fields_list)
        if not need_pagination:
            return list(enroll_obj), None
        # 分页展示
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_own_list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        enroll_obj = Enroll.objects.filter(**params).values()
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_edit(params=None, enroll_id=None, search_param=None):
        if not enroll_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"
        enroll_id = params.pop("enroll_id", None) or enroll_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "category_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code", "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount", "paid_amount", "unpaid_amount", "commision", "deposit",
                "bid_mode", "ticket", "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time", "create_time", "update_time", "snapshot", "remark",
            ],
        )
        enroll_obj = Enroll.objects
        if enroll_id:
            enroll_obj = enroll_obj.filter(id=enroll_id)
        if search_param:
            enroll_obj = enroll_obj.filter(**search_param)
        if not enroll_obj:
            return None, "找不到可修改的数据"

        try:
            enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return enroll_obj.first().to_json(), None

    @staticmethod
    def enroll_delete(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None
