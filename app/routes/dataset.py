from flask.views import MethodView

from app.extensions import db
from app.models import HousingModel
from app.models import LabourMarketModel
from app.models import TravelModel
from app.schemas.dataset import HousingDataBriefSchema
from app.schemas.dataset import HousingDataQuerySchema
from app.schemas.dataset import HousingDataSchema
from app.schemas.dataset import LabourMarketDataBriefSchema
from app.schemas.dataset import LabourMarketDataQuerySchema
from app.schemas.dataset import LabourMarketDataSchema
from app.schemas.dataset import TravelDataBriefSchema
from app.schemas.dataset import TravelDataQuerySchema
from app.schemas.dataset import TravelDataSchema
from . import dataset_bp


@dataset_bp.route('/housing', endpoint='housing_data_list')
class HousingDataList(MethodView):
    @dataset_bp.arguments(HousingDataQuerySchema, location='query')
    @dataset_bp.response(200, HousingDataBriefSchema(many=True))
    def get(self, args: dict):
        query = db.select(HousingModel)

        if args.get('year_lower'):
            query = query.where(HousingModel.year >= args['year_lower'])
        if args.get('year_upper'):
            query = query.where(HousingModel.year <= args['year_upper'])
        if args.get('month'):
            query = query.where(HousingModel.month == args['month'])

        return db.session.execute(
            query.order_by(HousingModel.year, HousingModel.month)
        ).scalars().all()


@dataset_bp.route('/housing/<int:sid>', endpoint='housing_data')
class HousingData(MethodView):
    @dataset_bp.response(200, HousingDataSchema)
    def get(self, sid):
        return db.one_or_404(
            db.select(HousingModel).where(HousingModel.sid == sid)
        )


@dataset_bp.route('/travel', endpoint='travel_data_list')
class TravelDataList(MethodView):
    @dataset_bp.arguments(TravelDataQuerySchema, location='query')
    @dataset_bp.response(200, TravelDataBriefSchema(many=True))
    def get(self, args: dict):
        query = db.select(TravelModel)

        if args.get('year_lower'):
            query = query.where(TravelModel.year >= args['year_lower'])
        if args.get('year_upper'):
            query = query.where(TravelModel.year <= args['year_upper'])
        if args.get('period'):
            query = query.where(TravelModel.period == args['period'])

        return db.session.execute(
            query.order_by(TravelModel.year, TravelModel.period)
        ).scalars().all()


@dataset_bp.route('/travel/<int:sid>', endpoint='travel_data')
class TravelData(MethodView):
    @dataset_bp.response(200, TravelDataSchema)
    def get(self, sid):
        return db.one_or_404(
            db.select(TravelModel).where(TravelModel.sid == sid)
        )


@dataset_bp.route('/labour-market', endpoint='labour_market_data_list')
class LabourMarketDataList(MethodView):
    @dataset_bp.arguments(LabourMarketDataQuerySchema, location='query')
    @dataset_bp.response(200, LabourMarketDataBriefSchema(many=True))
    def get(self, args: dict):
        query = db.select(LabourMarketModel)

        if args.get('year_lower'):
            query = query.where(LabourMarketModel.quarter_mid_y >= args['year_lower'])
        if args.get('year_upper'):
            query = query.where(LabourMarketModel.quarter_mid_y <= args['year_upper'])
        if args.get('month'):
            query = query.where(LabourMarketModel.quarter_mid_m == args['month'])

        return db.session.execute(
            query.order_by(LabourMarketModel.quarter_mid_y, LabourMarketModel.quarter_mid_m)
        ).scalars().all()


@dataset_bp.route('/labour-market/<int:sid>', endpoint='labour_market_data')
class LabourMarketData(MethodView):
    @dataset_bp.response(200, LabourMarketDataSchema)
    def get(self, sid):
        return db.one_or_404(
            db.select(LabourMarketModel).where(LabourMarketModel.sid == sid)
        )
