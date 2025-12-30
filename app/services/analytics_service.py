"""
Analytics Service - Business logic for data analysis
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.order import Order
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple, Optional
import pandas as pd


class AnalyticsService:
    """Analytics service for data analysis"""

    # ========== Helper Methods ==========

    @staticmethod
    def get_default_date_range() -> Tuple[date, date]:
        """Get default date range (last 30 days)"""
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        return start_date, end_date

    @staticmethod
    def validate_date_range(start_date: Optional[date], end_date: Optional[date]) -> Tuple[date, date]:
        """Validate and return date range"""
        if not start_date or not end_date:
            return AnalyticsService.get_default_date_range()

        if start_date > end_date:
            raise ValueError("start_date 必須早於或等於 end_date")

        if end_date > date.today():
            end_date = date.today()

        return start_date, end_date

    @staticmethod
    def get_orders_in_range(db: Session, start_date: date, end_date: date) -> List[Order]:
        """Get all orders within date range"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        return db.query(Order).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).all()

    # ========== Revenue Analysis ==========

    @staticmethod
    def get_daily_revenue(db: Session, start_date: date, end_date: date) -> Dict:
        """Get daily revenue breakdown"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        results = db.query(
            func.date(Order.created_at).label('date'),
            func.sum(Order.total_amount).label('revenue'),
            func.count(Order.id).label('order_count')
        ).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).group_by(
            func.date(Order.created_at)
        ).order_by(
            func.date(Order.created_at)
        ).all()

        data = [
            {
                'date': r.date,
                'revenue': r.revenue or 0,
                'order_count': r.order_count
            }
            for r in results
        ]

        total_revenue = sum(d['revenue'] for d in data)
        total_orders = sum(d['order_count'] for d in data)

        return {
            'period': 'daily',
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
            'total_revenue': total_revenue,
            'total_orders': total_orders
        }

    @staticmethod
    def get_weekly_revenue(db: Session, start_date: date, end_date: date) -> Dict:
        """Get weekly revenue breakdown"""
        orders = AnalyticsService.get_orders_in_range(db, start_date, end_date)

        if not orders:
            return {
                'period': 'weekly',
                'start_date': start_date,
                'end_date': end_date,
                'data': [],
                'total_revenue': 0,
                'total_orders': 0
            }

        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'date': o.created_at.date(),
                'revenue': o.total_amount,
                'order_id': o.id
            }
            for o in orders
        ])

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Resample by week
        weekly = df.resample('W').agg({
            'revenue': 'sum',
            'order_id': 'count'
        }).reset_index()

        data = [
            {
                'date': row['date'].date(),
                'revenue': int(row['revenue']),
                'order_count': int(row['order_id'])
            }
            for _, row in weekly.iterrows()
        ]

        return {
            'period': 'weekly',
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
            'total_revenue': sum(d['revenue'] for d in data),
            'total_orders': sum(d['order_count'] for d in data)
        }

    @staticmethod
    def get_monthly_revenue(db: Session, start_date: date, end_date: date) -> Dict:
        """Get monthly revenue breakdown"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        results = db.query(
            extract('year', Order.created_at).label('year'),
            extract('month', Order.created_at).label('month'),
            func.sum(Order.total_amount).label('revenue'),
            func.count(Order.id).label('order_count')
        ).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).group_by(
            extract('year', Order.created_at),
            extract('month', Order.created_at)
        ).order_by(
            extract('year', Order.created_at),
            extract('month', Order.created_at)
        ).all()

        data = [
            {
                'date': date(int(r.year), int(r.month), 1),
                'revenue': r.revenue or 0,
                'order_count': r.order_count
            }
            for r in results
        ]

        return {
            'period': 'monthly',
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
            'total_revenue': sum(d['revenue'] for d in data),
            'total_orders': sum(d['order_count'] for d in data)
        }

    @staticmethod
    def get_average_order_value(db: Session, start_date: date, end_date: date) -> Dict:
        """Calculate average order value"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        result = db.query(
            func.avg(Order.total_amount).label('avg_value'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_revenue')
        ).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).first()

        avg_value = float(result.avg_value) if result.avg_value else 0.0
        order_count = result.order_count or 0
        total_revenue = result.total_revenue or 0

        return {
            'start_date': start_date,
            'end_date': end_date,
            'average_order_value': round(avg_value, 2),
            'total_orders': order_count,
            'total_revenue': total_revenue
        }

    # ========== Popular Items Analysis ==========

    @staticmethod
    def get_popular_dishes(db: Session, start_date: date, end_date: date, limit: int = 10) -> Dict:
        """Get most popular dishes (non-drinks)"""
        orders = AnalyticsService.get_orders_in_range(db, start_date, end_date)

        # Aggregate dish data
        dish_stats = {}
        for order in orders:
            for item in order.items:
                item_id = item['id']
                if item_id not in dish_stats:
                    dish_stats[item_id] = {
                        'item_id': item_id,
                        'item_name': item['name'],
                        'total_quantity': 0,
                        'total_revenue': 0,
                        'order_count': 0
                    }
                dish_stats[item_id]['total_quantity'] += item['quantity']
                dish_stats[item_id]['total_revenue'] += item['price'] * item['quantity']
                dish_stats[item_id]['order_count'] += 1

        # Sort by quantity and take top N
        sorted_dishes = sorted(
            dish_stats.values(),
            key=lambda x: x['total_quantity'],
            reverse=True
        )[:limit]

        return {
            'category': 'dishes',
            'start_date': start_date,
            'end_date': end_date,
            'items': sorted_dishes
        }

    @staticmethod
    def get_popular_drinks(db: Session, start_date: date, end_date: date, limit: int = 10) -> Dict:
        """Get most popular drinks"""
        orders = AnalyticsService.get_orders_in_range(db, start_date, end_date)

        # Aggregate drink data
        drink_stats = {}
        for order in orders:
            if not order.drinks:
                continue
            for item in order.drinks:
                item_id = item['id']
                if item_id not in drink_stats:
                    drink_stats[item_id] = {
                        'item_id': item_id,
                        'item_name': item['name'],
                        'total_quantity': 0,
                        'total_revenue': 0,
                        'order_count': 0
                    }
                drink_stats[item_id]['total_quantity'] += item['quantity']
                drink_stats[item_id]['total_revenue'] += item['price'] * item['quantity']
                drink_stats[item_id]['order_count'] += 1

        # Sort by quantity and take top N
        sorted_drinks = sorted(
            drink_stats.values(),
            key=lambda x: x['total_quantity'],
            reverse=True
        )[:limit]

        return {
            'category': 'drinks',
            'start_date': start_date,
            'end_date': end_date,
            'items': sorted_drinks
        }

    # ========== Customer Behavior Analysis ==========

    @staticmethod
    def get_pickup_method_ratio(db: Session, start_date: date, end_date: date) -> Dict:
        """Analyze dine-in vs takeout ratio"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        results = db.query(
            Order.pickup_method,
            func.count(Order.id).label('count'),
            func.sum(Order.total_amount).label('revenue')
        ).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).group_by(
            Order.pickup_method
        ).all()

        total_orders = sum(r.count for r in results)

        stats = [
            {
                'pickup_method': r.pickup_method,
                'count': r.count,
                'percentage': round((r.count / total_orders * 100), 2) if total_orders > 0 else 0,
                'revenue': r.revenue or 0
            }
            for r in results
        ]

        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_orders': total_orders,
            'stats': stats
        }

    @staticmethod
    def get_peak_hours(db: Session, start_date: date, end_date: date) -> Dict:
        """Analyze peak hours of the day"""
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        results = db.query(
            extract('hour', Order.created_at).label('hour'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('revenue')
        ).filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        ).group_by(
            extract('hour', Order.created_at)
        ).order_by(
            extract('hour', Order.created_at)
        ).all()

        hourly_data = [
            {
                'hour': int(r.hour),
                'order_count': r.order_count,
                'revenue': r.revenue or 0
            }
            for r in results
        ]

        # Find peak hour
        peak_hour = max(hourly_data, key=lambda x: x['order_count']) if hourly_data else None

        return {
            'start_date': start_date,
            'end_date': end_date,
            'hourly_data': hourly_data,
            'peak_hour': peak_hour['hour'] if peak_hour else 0,
            'peak_hour_orders': peak_hour['order_count'] if peak_hour else 0
        }

    # ========== Beverage Preference Analysis ==========

    @staticmethod
    def get_ice_level_preferences(db: Session, start_date: date, end_date: date) -> Dict:
        """Analyze ice level preferences"""
        orders = AnalyticsService.get_orders_in_range(db, start_date, end_date)

        # Count ice level preferences
        ice_counts = {}
        total_drinks = 0

        for order in orders:
            if not order.drinks:
                continue
            for drink in order.drinks:
                if 'temperature' in drink and drink['temperature']:
                    temp = drink['temperature']
                    ice_counts[temp] = ice_counts.get(temp, 0) + drink['quantity']
                    total_drinks += drink['quantity']

        preferences = [
            {
                'option': option,
                'count': count,
                'percentage': round((count / total_drinks * 100), 2) if total_drinks > 0 else 0
            }
            for option, count in sorted(ice_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        most_popular = preferences[0]['option'] if preferences else 'N/A'

        return {
            'preference_type': 'ice_level',
            'start_date': start_date,
            'end_date': end_date,
            'total_drinks': total_drinks,
            'preferences': preferences,
            'most_popular': most_popular
        }

    @staticmethod
    def get_sweetness_preferences(db: Session, start_date: date, end_date: date) -> Dict:
        """Analyze sweetness preferences"""
        orders = AnalyticsService.get_orders_in_range(db, start_date, end_date)

        # Count sweetness preferences
        sweetness_counts = {}
        total_drinks = 0

        for order in orders:
            if not order.drinks:
                continue
            for drink in order.drinks:
                if 'sweetness' in drink and drink['sweetness']:
                    sweetness = drink['sweetness']
                    sweetness_counts[sweetness] = sweetness_counts.get(sweetness, 0) + drink['quantity']
                    total_drinks += drink['quantity']

        preferences = [
            {
                'option': option,
                'count': count,
                'percentage': round((count / total_drinks * 100), 2) if total_drinks > 0 else 0
            }
            for option, count in sorted(sweetness_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        most_popular = preferences[0]['option'] if preferences else 'N/A'

        return {
            'preference_type': 'sweetness',
            'start_date': start_date,
            'end_date': end_date,
            'total_drinks': total_drinks,
            'preferences': preferences,
            'most_popular': most_popular
        }
