from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product

def products(request, productName):
    # 产品类型映射（英文代码 -> 中文显示名称）
    product_type_mapping = {
        'robot': '牛客',
        'monitor': '学校OJ', 
        'face': 'VJudge'
    }
    
    # 获取中文显示名称，如果不存在则使用产品名称
    display_name = product_type_mapping.get(productName, productName)
    
    # 使用英文代码进行筛选，按发布时间降序排列
    product_list = Product.objects.filter(
        productType=productName
    ).order_by('-publishDate')
    
    # 分页设置
    paginator = Paginator(product_list, 2)
    page = request.GET.get('page', 1)
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，显示第一页
        products_page = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        products_page = paginator.page(paginator.num_pages)
    
    # 生成分页数据（简化版）
    page_data = generate_pagination_data(paginator, products_page.number)
    
    return render(
        request, 
        'productList.html', 
        {
            'active_menu': 'products',
            'sub_menu': productName,
            'productName': display_name,
            'productList': products_page,
            'pageData': page_data,
        }
    )

def generate_pagination_data(paginator, current_page):
    """生成分页导航数据"""
    total_pages = paginator.num_pages
    page_range = list(paginator.page_range)
    
    if total_pages <= 1:
        return {}
    
    # 设置左右显示的页码数量
    left_count = 2
    right_count = 2
    
    left = []
    right = []
    left_has_more = False
    right_has_more = False
    first = False
    last = False
    
    if current_page == 1:
        # 第一页
        right = page_range[current_page:current_page + right_count]
        if right and right[-1] < total_pages - 1:
            right_has_more = True
        if right and right[-1] < total_pages:
            last = True
    elif current_page == total_pages:
        # 最后一页
        left_start = max(0, current_page - left_count - 1)
        left = page_range[left_start:current_page - 1]
        if left and left[0] > 2:
            left_has_more = True
        if left and left[0] > 1:
            first = True
    else:
        # 中间页
        left_start = max(0, current_page - left_count - 1)
        left = page_range[left_start:current_page - 1]
        right = page_range[current_page:current_page + right_count]
        
        if left and left[0] > 2:
            left_has_more = True
        if left and left[0] > 1:
            first = True
        if right and right[-1] < total_pages - 1:
            right_has_more = True
        if right and right[-1] < total_pages:
            last = True
    
    return {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
        'total_pages': total_pages,
        'page': current_page,
    }
# productsApp/views.py
from django.http import Http404
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return render(request, 'productDetail.html', {
            'active_menu': 'products',
            'product': product,
        })
    except Product.DoesNotExist:
        raise Http404("产品不存在")