import paypalrestsdk
from django.utils import timezone

from app import settings
from app.utils import add_months
from guardians.models import Guardian
from payments.card import Card
from payments.models import Order, OrderDetail, PaypalTransaction, PaymentMethod, CardTransaction, DiscountCode
from payments.paypal import Paypal
from plans.models import Plan, GuardianStudentPlan
from app.utils import add_months


class TmpOrderDetail:
    plan: Plan
    period: str
    quantity: int

    def __init__(self, plan: Plan, period: str, quantity: int):
        self.plan = plan
        self.period = period
        self.quantity = quantity


class CreateOrderResp:
    url_redirect: str
    order: Order

    def __init__(self, url_redirect: str, order: Order):
        self.url_redirect = url_redirect
        self.order = order


# ----------------- Payment Method Service ----------------- #


def check_is_duplicate(
        method: str,
        guardian_id,
        card_number=None,
        card_cvc=None,
        card_first_name=None,
        card_last_name=None,
        card_exp_month=None,
        card_exp_year=None,
        address1=None,
        address2=None,
        city=None,
        state=None,
        post_code=None,
        country=None,
        phone=None,
):
    # get all guardian payment method
    payment_methods = PaymentMethod.objects.filter(
        guardian_id=guardian_id,
        method=method,
        card_number=card_number,
        card_cvc=card_cvc,
        card_first_name=card_first_name,
        card_last_name=card_last_name,
        card_exp_month=card_exp_month,
        card_exp_year=card_exp_year,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        phone=phone
    )

    has_info = False
    obj_id = 0

    if len(payment_methods) > 0:
        has_info = True
        obj_id = payment_methods.first().id

    return{
        "status": has_info,
        "id": obj_id
    }


def add_or_update_payment_method(
     method: str,
     guardian_id,
     card_first_name=None,
     card_last_name=None,
     card_number=None,
     card_exp_month=None,
     card_exp_year=None,
     card_cvc=None,
     address1=None,
     address2=None,
     city=None,
     state=None,
     post_code=None,
     country=None,
     phone=None,
) -> str:
    method = method.upper()
    if method == "CARD" and card_number is None and card_cvc is None:
        return "cannot create card with no card number"

    # get all guardian payment method
    payment_methods = PaymentMethod.objects.filter(guardian_id=guardian_id)
    is_default = False
    has_info = check_is_duplicate(
        method=method,
        guardian_id=guardian_id,
        card_number=card_number,
        card_cvc=card_cvc,
        card_exp_month=card_exp_month,
        card_exp_year=card_exp_year,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        phone=phone
    )

    if has_info["status"]:
        return "has already"

    if len(payment_methods) == 0:
        is_default = True

    # create payment method
    PaymentMethod.objects.create(
        guardian_id=guardian_id,
        method=method,
        card_first_name=card_first_name,
        card_last_name=card_last_name,
        card_number=card_number,
        card_exp_month=card_exp_month,
        card_exp_year=card_exp_year,
        card_cvc=card_cvc,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        phone=phone,
        is_default=is_default
    )
    return "created"


def change_default_payment_method(
        method: str,
        guardian_id,
        card_first_name=None,
        card_last_name=None,
        card_number=None,
        card_exp_month=None,
        card_exp_year=None,
        card_cvc=None,
        address1=None,
        address2=None,
        city=None,
        state=None,
        post_code=None,
        country=None,
        phone=None,
):
    method = method.upper()
    has_info = check_is_duplicate(
        method=method,
        guardian_id=guardian_id,
        card_first_name=card_first_name,
        card_last_name=card_last_name,
        card_number=card_number,
        card_exp_month=card_exp_month,
        card_exp_year=card_exp_year,
        card_cvc=card_cvc,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        phone=phone,
    )

    payment_methods = PaymentMethod.objects.filter(guardian_id=guardian_id)
    for payment_method in payment_methods:
        payment_method.is_default = False
        payment_method.save()

    if has_info["status"]:
        obj = PaymentMethod.objects.get(pk=has_info["id"])
        obj.is_default = True
        obj.save()
        return
    PaymentMethod.objects.create(
        guardian_id=guardian_id,
        method=method,
        card_first_name=card_first_name,
        card_last_name=card_last_name,
        card_number=card_number,
        card_exp_month=card_exp_month,
        card_exp_year=card_exp_year,
        card_cvc=card_cvc,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        phone=phone,
        is_default=True
    )
    return


def edit_payment_method(
        payment_method_id,
        card_first_name=None,
        card_last_name=None,
        card_number=None,
        card_exp_month=None,
        card_exp_year=None,
        card_cvc=None,
        address1=None,
        address2=None,
        city=None,
        state=None,
        post_code=None,
        country=None,
        phone=None,
):

    payment_method = PaymentMethod.objects.get(pk=payment_method_id)
    payment_method.card_first_name = card_first_name
    payment_method.card_last_name = card_last_name
    payment_method.card_number = card_number
    payment_method.card_exp_month = card_exp_month
    payment_method.card_exp_year = card_exp_year
    payment_method.card_cvc = card_cvc
    payment_method.address1 = address1
    payment_method.address2 = address2
    payment_method.city = city
    payment_method.state = state
    payment_method.post_code = post_code
    payment_method.country = country
    payment_method.phone = phone
    payment_method.save()
    return payment_method.guardian.id


def change_order_detail_payment_method(guardian_id) -> Guardian:
    guardian = Guardian.objects.get(pk=guardian_id)
    payment_method = PaymentMethod.objects.get(guardian_id=guardian_id, is_default=True)
    order_details = OrderDetail.objects.filter(order__guardian_id=guardian.id, is_cancel=False)
    for order_detail in order_details:
        if order_detail.order.payment_method == "CARD":
            card = Card()
            card.change_payment_method(
                sub_id=order_detail.subscription_id,
                number=payment_method.card_number,
                exp_month=payment_method.card_exp_month,
                exp_year=payment_method.card_exp_year,
                cvc=payment_method.card_cvc,
                first_name=payment_method.card_first_name,
                last_name=payment_method.card_last_name,
                address1=payment_method.address1,
                address2=payment_method.address2,
                city=payment_method.city,
                state=payment_method.state,
                country=payment_method.country,
                post_code=payment_method.post_code,
                email=order_detail.order.guardian.user.email,
                phone=payment_method.phone
            )
    return guardian


# ----------------- Create Order Service ----------------- #


def payment_card_subscription(
        order_detail: OrderDetail,
        customer_id: str,
        has_order: bool
):
    card = Card()
    # payment_method = card.create_payment_method(
    #     number=card_number,
    #     exp_month=card_exp_month,
    #     exp_year=card_exp_year,
    #     cvc=card_cvc,
    #     first_name=first_name,
    #     last_name=last_name,
    #     address1=address1,
    #     address2=address2,
    #     city=city,
    #     country=country,
    #     post_code=post_code,
    #     state=state,
    #     phone=phone,
    #     email=email
    # )

    # customer = card.create_customer(
    #     email,
    #     payment_method_id=payment_method.id
    # )

    # get a coupon if has
    coupon_id = None
    trial_day = 0
    if order_detail.order.discount_code != "" and order_detail.order.discount_code is not None:
        discount_code = DiscountCode.objects.get(code=order_detail.order.discount_code)
        trial_day = discount_code.trial_day
        if discount_code.percentage > 0:
            coupon_id = card.create_or_get_coupon(code=discount_code.code, percentage=discount_code.percentage)

    sub = card.create_subscription(
        customer_id=customer_id,
        plan_id=order_detail.payment_method_plan_id,
        quantity=order_detail.quantity,
        has_order=has_order,
        coupon_id=coupon_id,
        trial_day=trial_day
    )
    return sub


def create_order(guardian_id,
                 discount_code,
                 discount,
                 sub_total,
                 total,
                 payment_method,
                 order_detail_list,
                 return_url,
                 card_first_name=None,
                 card_last_name=None,
                 card_number=None,
                 card_exp_month=None,
                 card_exp_year=None,
                 card_cvc=None,
                 address1=None,
                 address2=None,
                 city=None,
                 state=None,
                 post_code=None,
                 country=None,
                 phone=None,
                 order_detail_id=0
                 ) -> CreateOrderResp:

    guardian = Guardian.objects.get(pk=guardian_id)
    payment_method = payment_method.upper()

    if payment_method != "CARD" and payment_method != "PAYPAL" and payment_method != "APPLEPAY":
        raise Exception("need payment method enum Card, PayPal, ApplePay.")

    if payment_method == "CARD" and card_number is None and card_exp_month is None and card_exp_year is None and card_cvc is None:
        raise Exception("need card information")

    sub_total = 0
    total = 0

    # create order
    order = Order.objects.create(
        discount_code='',
        guardian_id=guardian.id,
        payment_method=payment_method
    )

    # sorted input by DESC
    tmp_order_details = []
    for order_detail in order_detail_list:
        plan = Plan.objects.get(pk=order_detail.plan_id)
        tmp_order_details.append(
            TmpOrderDetail(plan=plan, period=order_detail.period.upper(), quantity=order_detail.quantity)
        )
    tmp_order_details.sort(key=lambda x: x.plan.price_month, reverse=True)

    # go through order detail
    for index, tmp_order_detail in enumerate(tmp_order_details):

        order_detail_price = 0
        more_than_two = tmp_order_detail.quantity - 1

        # check if first index then calculate normal
        # if index == 0:
        #     if tmp_order_detail.period == "MONTHLY":
        #         order_detail_price += (tmp_order_detail.plan.price_month + more_than_two * (tmp_order_detail.plan.price_month / 2))
        #     else:
        #         order_detail_price += (tmp_order_detail.plan.price_year + more_than_two * (tmp_order_detail.plan.price_year / 2))
        # else:
        #     if tmp_order_detail.period == "MONTHLY":
        #         order_detail_price += tmp_order_detail.quantity * (tmp_order_detail.plan.price_month / 2)
        #     else:
        #         order_detail_price += tmp_order_detail.quantity * (tmp_order_detail.plan.price_year / 2)

        if tmp_order_detail.period == "MONTHLY":
            order_detail_price += tmp_order_detail.plan.price_month if(tmp_order_detail.quantity == 1) else tmp_order_detail.quantity * (tmp_order_detail.plan.price_month / 2)
        else:
            order_detail_price += tmp_order_detail.plan.price_year if(tmp_order_detail.quantity == 1) else tmp_order_detail.quantity * (tmp_order_detail.plan.price_year / 2)

        # # check plan payment id by payment_method
        # payment_method_plan_id = ""
        # if order.payment_method == "CARD":
        #     if index == 0:
        #         if tmp_order_detail.period == "MONTHLY":
        #             payment_method_plan_id = tmp_order_detail.plan.stripe_monthly_plan_id
        #         else:
        #             payment_method_plan_id = tmp_order_detail.plan.stripe_yearly_plan_id
        #     else:
        #         if tmp_order_detail.period == "MONTHLY":
        #             payment_method_plan_id = tmp_order_detail.plan.stripe_monthly_plan_half_price_id
        #         else:
        #             payment_method_plan_id = tmp_order_detail.plan.stripe_yearly_plan_half_price_id

        if order.payment_method == "CARD":
            if tmp_order_detail.period == "MONTHLY":
                payment_method_plan_id = tmp_order_detail.plan.stripe_monthly_plan_id if(tmp_order_detail.quantity == 1) else tmp_order_detail.plan.stripe_monthly_plan_half_price_id
            else:
                payment_method_plan_id = tmp_order_detail.plan.stripe_yearly_plan_id if(tmp_order_detail.quantity == 1) else tmp_order_detail.plan.stripe_yearly_plan_half_price_id


        # calculate sub_total and total price before add to order
        sub_total += order_detail_price
        total += order_detail_price

        # create order detail
        OrderDetail.objects.create(
            plan_id=tmp_order_detail.plan.id,
            payment_method_plan_id=payment_method_plan_id,
            quantity=tmp_order_detail.quantity,
            total=order_detail_price,
            order_id=order.id,
            period=tmp_order_detail.period,
            update_from_detail_id=order_detail_id
        )

    order.sub_total = sub_total

    # calculate discount
    if discount_code:
        code = DiscountCode.objects.filter(code=discount_code)
        if len(code) > 0:
            code = code.first()
            discount_price = (code.percentage/100) * sub_total
            total = total - discount_price
            order.discount_code = code.code
            order.discount = discount_price
    elif guardian.coupon_code:
        discount_price = (guardian.coupon_code.percentage / 100) * sub_total
        total = total - discount_price
        order.discount_code = guardian.coupon_code.code
        order.discount = discount_price


    order.total = total
    order.save()

    url_redirect = ""
    if order.payment_method.upper() == "PAYPAL":
        paypal = Paypal()
        paypal_tx = paypal.create_sub("https://www.example.com/", "https://www.example.com/", 2, order_id=order.id)
        url_redirect = paypal_tx.approve_link
    elif order.payment_method.upper() == "CARD":
        order_details = OrderDetail.objects.filter(order_id=order.id)

        card = Card()
        
        # --------------------- create Customer to parent and attach payment method -S-----------------#
        guardian = Guardian.objects.get(pk = guardian_id)
        user = guardian.user

        if(not user.stripe_customer_id):
            payment_method = card.create_payment_method(
                number=card_number,
                exp_month=card_exp_month,
                exp_year=card_exp_year,
                cvc=card_cvc,
                first_name=card_first_name,
                last_name=card_last_name,
                address1=address1,
                address2=address2,
                city=city,
                country=country,
                post_code=post_code,
                state=state,
                phone=phone,
                email=order.guardian.user.email,
            )    
            customer = card.create_customer(
                order.guardian.user.email,
                payment_method_id=payment_method.id
            )
            user.stripe_customer_id = customer.id
            user.save()
        else:
            card.change_payment_method(
                customer_id=user.stripe_customer_id,
                number=card_number,
                exp_month=card_exp_month,
                exp_year=card_exp_year,
                cvc=card_cvc,
                first_name=card_first_name,
                last_name=card_last_name,
                address1=address1,
                address2=address2,
                city=city,
                country=country,
                post_code=post_code,
                state=state,
                phone=phone,
                email=order.guardian.user.email,
            )
        # --------------------- create Customer to parent and attach payment method -E-----------------#

        for order_detail in order_details:
            sub = payment_card_subscription(
                order_detail=order_detail,
                customer_id=user.stripe_customer_id,
                has_order=order.guardian.has_order
            )
            order_detail.subscription_id = sub.id
            order_detail.save()

            # create card transaction
            CardTransaction.objects.create(
                order_detail_id=order_detail.id,
                session_id=sub.latest_invoice,
                card_first_name=card_first_name,
                card_last_name=card_last_name,
                card_number=card_number,
                card_exp_month=card_exp_month,
                card_exp_year=card_exp_year,
                card_cvc=card_cvc,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                post_code=post_code,
                country=country,
                phone=phone,
                approve_link="-"
            )
        url_redirect = "card.url_redirect"

        order_from_db = Order.objects.get(pk=order.id)

    return CreateOrderResp(url_redirect=url_redirect, order=order_from_db)


def confirm_order_payment(
        order_id,
        first_name=None,
        last_name=None,
        address1=None,
        address2=None,
        city=None,
        state=None,
        post_code=None,
        country=None,
        phone=None
) -> Order:
    order = Order.objects.get(pk=order_id)

    if order.is_paid:
        raise Exception("This order already been paid.")

    all_paid = True

    # Confirm payment by method type
    if order.payment_method.upper() == "PAYPAL":
        paypal_tx = PaypalTransaction.objects.get(order_id=order.id)
        paypal = Paypal()
        paypal.get_token()
        tx = paypal.capture_sub(paypal_tx.token_id)
        if tx != "paid":
            raise Exception("unpaid")
    elif order.payment_method.upper() == "CARD":
        card = Card()
        order_details = OrderDetail.objects.filter(order_id=order_id)
        for order_detail in order_details:
            card_tx = CardTransaction.objects.get(order_detail_id=order_detail.id)
            result_sub = card.check_subscription(order_detail.subscription_id)
            if result_sub["status"] != "active" and result_sub["status"] != "trialing":
                all_paid = False
                raise Exception(f"unpaid for card in sub_id: {order_detail.subscription_id}")
            result = add_or_update_payment_method(
                method="CARD",
                guardian_id=order_detail.order.guardian.id,
                card_first_name=card_tx.card_first_name,
                card_last_name=card_tx.card_last_name,
                card_number=card_tx.card_number,
                card_exp_month=card_tx.card_exp_month,
                card_exp_year=card_tx.card_exp_year,
                card_cvc=card_tx.card_cvc,
                address1=card_tx.address1,
                address2=card_tx.address2,
                city=card_tx.city,
                state=card_tx.state,
                post_code=card_tx.post_code,
                country=card_tx.country,
                phone=card_tx.phone
            )
            order_detail.status = result_sub["status"]
            order_detail.expired_at = result_sub["expired_at"]
            order_detail.is_paid = True
            order_detail.save()
    elif order.payment_method.upper() == "FREE":
        order_details = OrderDetail.objects.filter(order_id=order_id)
        for order_detail in order_details:
            order_detail.status = "active"

            add_or_update_payment_method(
                method="FREE",
                guardian_id=order_detail.order.guardian.id,
                card_first_name=first_name,
                card_last_name=last_name,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                post_code=post_code,
                country=country,
                phone=phone
            )

            if order_detail.period == "MONTHLY":
                expired_date = add_months(order_detail.create_timestamp, 1)
            else:
                expired_date = add_months(order_detail.create_timestamp, 1)

            order_detail.expired_at = expired_date
            order_detail.is_paid = True
            order_detail.save()


    # change order paid status to true
    order.is_paid = True
    order.save()

    # update guardian status order
    guardian = Guardian.objects.get(pk=order.guardian.id)
    guardian.coupon_code = None
    guardian.has_order = True
    guardian.save()

    return order


def check_order_detail(order_detail_id) -> OrderDetail:

    order_detail = OrderDetail.objects.get(pk=order_detail_id)

    old_payment = order_detail.order.payment_method

    if old_payment == "CARD":
        card = Card()
        resp = card.check_subscription(order_detail.subscription_id)
        order_detail.status = resp["status"]
        order_detail.expired_at = resp["expired_at"]

        if resp["status"] == "canceled":
            order_detail.is_cancel = True
    elif old_payment == "FREE":
        if timezone.now() > order_detail.expired_at:
            order_detail.status = "canceled"
            order_detail.is_cancel = True

    order_detail.save()

    return order_detail


def create_order_with_out_pay(
        guardian_id,
        order_detail_list,
) -> CreateOrderResp:

    guardian = Guardian.objects.get(pk=guardian_id)

    sub_total = 0
    total = 0

    # create order
    order = Order.objects.create(
        discount_code='',
        guardian_id=guardian.id,
        payment_method="FREE"
    )

    # sorted input by DESC
    tmp_order_details = []
    for order_detail in order_detail_list:
        plan = Plan.objects.get(pk=order_detail.plan_id)
        tmp_order_details.append(
            TmpOrderDetail(plan=plan, period=order_detail.period.upper(), quantity=order_detail.quantity)
        )
    tmp_order_details.sort(key=lambda x: x.plan.price_month, reverse=True)

    # go through order detail
    for index, tmp_order_detail in enumerate(tmp_order_details):

        order_detail_price = 0
        more_than_two = tmp_order_detail.quantity - 1

        # check if first index then calculate normal
        if index == 0:
            if tmp_order_detail.period == "MONTHLY":
                order_detail_price += (tmp_order_detail.plan.price_month + more_than_two * (tmp_order_detail.plan.price_month / 2))
            else:
                order_detail_price += (tmp_order_detail.plan.price_year + more_than_two * (tmp_order_detail.plan.price_year / 2))
        else:
            if tmp_order_detail.period == "MONTHLY":
                order_detail_price += tmp_order_detail.quantity * (tmp_order_detail.plan.price_month / 2)
            else:
                order_detail_price += tmp_order_detail.quantity * (tmp_order_detail.plan.price_year / 2)

        # check plan payment id by payment_method
        payment_method_plan_id = ""

        # calculate sub_total and total price before add to order
        sub_total += order_detail_price
        total += order_detail_price

        # create order detail
        OrderDetail.objects.create(
            plan_id=tmp_order_detail.plan.id,
            payment_method_plan_id=payment_method_plan_id,
            quantity=tmp_order_detail.quantity,
            total=order_detail_price,
            order_id=order.id,
            period=tmp_order_detail.period,
            update_from_detail_id=0
        )

    order.sub_total = sub_total

    order.total = total
    order.save()

    if guardian.coupon_code:
        order.discount_code = guardian.coupon_code.code
        order.save()

    order_from_db = Order.objects.get(pk=order.id)

    return CreateOrderResp(url_redirect="", order=order_from_db)
