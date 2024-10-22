-- DROP FUNCTION public.get_stock_data(integer[], integer[], integer[], integer[], text, date, date);
CREATE OR REPLACE FUNCTION public.get_stock_data(
    IN company_ids integer[],
    IN product_ids integer[],
    IN category_ids integer[],
    IN warehouse_ids integer[],
    IN transaction_type text,
    IN start_date date,
    IN end_date date)
  RETURNS TABLE(company_id integer, company_name character varying, product_id integer, product_name character varying, product_category_id integer, category_name character varying, warehouse_id integer, warehouse_name character varying, product_qty numeric) AS
$BODY$
DECLARE
    source_usage text[];
    dest_usage text[];
    tr_start_date timestamp without time zone := (start_date || ' 00:00:00')::timestamp without time zone;
    tr_end_date timestamp without time zone:= (end_date || ' 23:59:59')::timestamp without time zone;
BEGIN
    source_usage := case
                when transaction_type in ('sales','transit_out','production_out','internal_out', 'adjustment_out', 'internal_in','purchase_return')
                    then array['internal', 'view']
                when transaction_type = 'purchase' then array['supplier']
                when transaction_type = 'transit_in' then array['transit']
                when transaction_type = 'adjustment_in' then array['inventory']
                when transaction_type = 'production_in' then array['production']
                when transaction_type = 'sales_return' then array['customer']
            end;
    dest_usage := case
                when transaction_type in ('purchase','transit_in','adjustment_in','production_in', 'internal_in', 'internal_out', 'sales_return')
                    then array['internal', 'view']
                when transaction_type = 'sales' then array['customer']
                when transaction_type = 'transit_out' then array['transit']
                when transaction_type = 'adjustment_out' then array['inventory']
                when transaction_type = 'production_out' then array['production']
                when transaction_type = 'purchase_return' then array['supplier']
            end;

    RETURN QUERY
    Select
        T.company_id,
        T.company_name,
        T.product_id,
        T.product_name,
        T.category_id,
        T.category_name,
        T.warehouse_id,
        T.warehouse_name,
        coalesce(sum(T.product_qty),0) as product_qty
    From
    (
        Select
            move.company_id,
            cmp.name as company_name,
            move.product_id as product_id,
            --prod.default_code as product_name,
            case when prod.default_code is not null then
                ('['||prod.default_code||']'||' '||tmpl.name) else tmpl.name end as product_name,
            --coalesce(prod.default_code, tmpl.name) as product_name,
            tmpl.categ_id as category_id,
            cat.complete_name as category_name,
            case when transaction_type in ('sales','transit_out','production_out','internal_out', 'adjustment_out', 'purchase_return') then
                source_warehouse.id else  dest_warehouse.id end as warehouse_id,
            case when transaction_type in ('sales','transit_out','production_out','internal_out', 'adjustment_out', 'purchase_return') then
                source_warehouse.name else  dest_warehouse.name end as warehouse_name,
--            sum(sml.qty_done) as product_qty
            move.product_uom_qty as product_qty
        From
            stock_move move
--                Inner Join stock_move_line sml on sml.move_id = move.id
                Inner Join stock_location source on source.id = move.location_id
                Inner Join stock_location dest on dest.id = move.location_dest_id
                Inner Join res_company cmp on cmp.id = move.company_id
                Inner Join product_product prod on prod.id = move.product_id
                Inner Join product_template tmpl on tmpl.id = prod.product_tmpl_id and tmpl.detailed_type = 'product'
                Inner Join product_category cat on cat.id = tmpl.categ_id
                Left Join stock_warehouse source_warehouse ON source.parent_path::text ~~ concat('%/', source_warehouse.view_location_id, '/%')
                Left Join stock_warehouse dest_warehouse ON dest.parent_path::text ~~ concat('%/', dest_warehouse.view_location_id, '/%')
        where prod.active = true and tmpl.active = true
        and source.usage = ANY(source_usage) and dest.usage = ANY(dest_usage)
        and move.date::date >= tr_start_date and move.date::date <= tr_end_date
        and move.state = 'done'
        and tmpl.type = 'product'

        --company dynamic condition
        and 1 = case when array_length(company_ids,1) >= 1 then
            case when move.company_id = ANY(company_ids) then 1 else 0 end
            else 1 end
        --product dynamic condition
        and 1 = case when array_length(product_ids,1) >= 1 then
            case when move.product_id = ANY(product_ids) then 1 else 0 end
            else 1 end
        --category dynamic condition
        and 1 = case when array_length(category_ids,1) >= 1 then
            case when tmpl.categ_id = ANY(category_ids) then 1 else 0 end
            else 1 end
        --warehouse dynamic condition
        and 1 = case when array_length(warehouse_ids,1) >= 1 then
                case when transaction_type in ('sales','transit_out','production_out','internal_out', 'adjustment_out','purchase_return'	) then
                    case when source_warehouse.id = ANY(warehouse_ids) then 1 else 0 end
                else
                    case when dest_warehouse.id = ANY(warehouse_ids) then 1 else 0 end
                end
            else 1 end
        --group by move.company_id, cmp.name, move.product_id, prod.default_code, tmpl.name, tmpl.categ_id, cat.complete_name, source_warehouse.id, source_warehouse.name, dest_warehouse.id, dest_warehouse.name, move.id
    )T
    group by T.company_id, T.product_id, T.category_id, T.warehouse_id, T.company_name, T.product_name, T.category_name, T.warehouse_name
    ;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
